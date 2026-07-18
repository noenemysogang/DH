"""Deterministic financial variance analysis for review-ready Markdown reports."""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Iterable, Sequence


REQUIRED_COLUMNS = ("account", "current", "prior")


@dataclass(frozen=True)
class FinancialRow:
    account: str
    current: Decimal
    prior: Decimal


@dataclass(frozen=True)
class Finding:
    account: str
    current: Decimal
    prior: Decimal
    change: Decimal
    percent_change: Decimal | None


def parse_decimal(value: str) -> Decimal:
    cleaned = value.strip().replace(",", "")
    if cleaned.startswith("(") and cleaned.endswith(")"):
        cleaned = f"-{cleaned[1:-1]}"
    if not cleaned:
        raise ValueError("amount is empty")
    try:
        return Decimal(cleaned)
    except InvalidOperation as exc:
        raise ValueError(f"invalid amount: {value!r}") from exc


def read_financial_rows(path: Path) -> list[FinancialRow]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = tuple(reader.fieldnames or ())
        missing = [name for name in REQUIRED_COLUMNS if name not in fieldnames]
        if missing:
            raise ValueError(f"missing required columns: {', '.join(missing)}")

        rows: list[FinancialRow] = []
        for line_number, raw in enumerate(reader, start=2):
            account = (raw.get("account") or "").strip()
            if not account:
                raise ValueError(f"line {line_number}: account is empty")
            try:
                current = parse_decimal(raw.get("current") or "")
                prior = parse_decimal(raw.get("prior") or "")
            except ValueError as exc:
                raise ValueError(f"line {line_number}: {exc}") from exc
            rows.append(FinancialRow(account=account, current=current, prior=prior))
    return rows


def analyze_variances(
    rows: Iterable[FinancialRow],
    percent_threshold: Decimal,
    amount_threshold: Decimal,
) -> list[Finding]:
    if percent_threshold < 0:
        raise ValueError("percent threshold must be non-negative")
    if amount_threshold < 0:
        raise ValueError("amount threshold must be non-negative")

    findings: list[Finding] = []
    for row in rows:
        change = row.current - row.prior
        percent_change = None if row.prior == 0 else change / abs(row.prior)
        meets_percent = (
            row.current != 0 if percent_change is None else abs(percent_change) >= percent_threshold
        )
        if abs(change) >= amount_threshold and meets_percent:
            findings.append(
                Finding(
                    account=row.account,
                    current=row.current,
                    prior=row.prior,
                    change=change,
                    percent_change=percent_change,
                )
            )
    return sorted(findings, key=lambda item: abs(item.change), reverse=True)


def _format_amount(value: Decimal) -> str:
    return f"{value:,.2f}"


def _format_percent(value: Decimal | None, locale: str) -> str:
    if value is None:
        return "N/A" if locale == "en" else "신규"
    return f"{value * 100:.1f}%"


def _escape_markdown(value: str) -> str:
    return value.replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ")


def render_markdown(
    findings: Sequence[Finding],
    source_name: str,
    locale: str = "ko",
) -> str:
    if locale not in {"ko", "en"}:
        raise ValueError("locale must be 'ko' or 'en'")

    if locale == "ko":
        title = "재무 변동 검토 보고서"
        summary = f"검토 대상: `{_escape_markdown(source_name)}` | 중요 변동: **{len(findings)}건**"
        headers = ("계정", "당기", "전기", "증감", "증감률")
        empty = "설정된 기준을 초과한 변동이 없습니다."
    else:
        title = "Financial Variance Review"
        summary = f"Source: `{_escape_markdown(source_name)}` | Flagged variances: **{len(findings)}**"
        headers = ("Account", "Current", "Prior", "Change", "Change %")
        empty = "No variances exceeded the configured thresholds."

    lines = [f"# {title}", "", summary, ""]
    if not findings:
        lines.append(empty)
        return "\n".join(lines) + "\n"

    lines.extend(
        [
            f"| {' | '.join(headers)} |",
            f"| {' | '.join(['---'] * len(headers))} |",
        ]
    )
    for finding in findings:
        lines.append(
            "| "
            + " | ".join(
                (
                    _escape_markdown(finding.account),
                    _format_amount(finding.current),
                    _format_amount(finding.prior),
                    _format_amount(finding.change),
                    _format_percent(finding.percent_change, locale),
                )
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a deterministic Markdown report from financial CSV data."
    )
    parser.add_argument("input", type=Path, help="CSV with account,current,prior columns")
    parser.add_argument("-o", "--output", type=Path, help="Markdown output path; defaults to stdout")
    parser.add_argument(
        "--percent-threshold",
        type=Decimal,
        default=Decimal("20"),
        help="minimum absolute percentage change to flag (default: 20)",
    )
    parser.add_argument(
        "--amount-threshold",
        type=Decimal,
        default=Decimal("0"),
        help="minimum absolute amount change to flag (default: 0)",
    )
    parser.add_argument("--locale", choices=("ko", "en"), default="ko")
    parser.add_argument("--top", type=int, help="limit the report to the largest N changes")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.top is not None and args.top < 1:
        parser.error("--top must be at least 1")

    try:
        rows = read_financial_rows(args.input)
        findings = analyze_variances(
            rows,
            percent_threshold=args.percent_threshold / Decimal("100"),
            amount_threshold=args.amount_threshold,
        )
        if args.top is not None:
            findings = findings[: args.top]
        report = render_markdown(findings, args.input.name, args.locale)
        if args.output:
            args.output.write_text(report, encoding="utf-8")
        else:
            sys.stdout.write(report)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
