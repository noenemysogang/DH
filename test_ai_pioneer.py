from __future__ import annotations

import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from ai_pioneer import (
    FinancialRow,
    analyze_variances,
    main,
    parse_decimal,
    read_financial_rows,
    render_markdown,
)


class ParseDecimalTests(unittest.TestCase):
    def test_accepts_commas_and_parentheses(self) -> None:
        self.assertEqual(parse_decimal("1,234.50"), Decimal("1234.50"))
        self.assertEqual(parse_decimal("(250)"), Decimal("-250"))

    def test_rejects_empty_or_invalid_amounts(self) -> None:
        with self.assertRaisesRegex(ValueError, "empty"):
            parse_decimal(" ")
        with self.assertRaisesRegex(ValueError, "invalid"):
            parse_decimal("not-a-number")


class AnalysisTests(unittest.TestCase):
    def test_applies_both_amount_and_percent_thresholds(self) -> None:
        rows = [
            FinancialRow("Revenue", Decimal("140"), Decimal("100")),
            FinancialRow("Cash", Decimal("105"), Decimal("100")),
            FinancialRow("Inventory", Decimal("125"), Decimal("100")),
        ]
        findings = analyze_variances(rows, Decimal("0.20"), Decimal("30"))
        self.assertEqual([item.account for item in findings], ["Revenue"])

    def test_flags_new_nonzero_balance(self) -> None:
        rows = [FinancialRow("New account", Decimal("50"), Decimal("0"))]
        findings = analyze_variances(rows, Decimal("0.20"), Decimal("10"))
        self.assertEqual(len(findings), 1)
        self.assertIsNone(findings[0].percent_change)

    def test_sorts_by_absolute_change(self) -> None:
        rows = [
            FinancialRow("A", Decimal("130"), Decimal("100")),
            FinancialRow("B", Decimal("20"), Decimal("100")),
        ]
        findings = analyze_variances(rows, Decimal("0.20"), Decimal("0"))
        self.assertEqual([item.account for item in findings], ["B", "A"])


class InputAndOutputTests(unittest.TestCase):
    def test_reads_utf8_csv_and_reports_line_errors(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "input.csv"
            path.write_text("account,current,prior\nRevenue,120,100\n", encoding="utf-8")
            self.assertEqual(read_financial_rows(path)[0].account, "Revenue")
            path.write_text("account,current,prior\n,120,100\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "line 2"):
                read_financial_rows(path)

    def test_markdown_escapes_account_names(self) -> None:
        findings = analyze_variances(
            [FinancialRow("A|B", Decimal("200"), Decimal("100"))],
            Decimal("0.20"),
            Decimal("0"),
        )
        report = render_markdown(findings, "sample.csv", "en")
        self.assertIn("A\\|B", report)
        self.assertIn("100.0%", report)

    def test_cli_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "input.csv"
            output = Path(temp_dir) / "report.md"
            source.write_text("account,current,prior\nRevenue,140,100\n", encoding="utf-8")
            code = main([str(source), "-o", str(output), "--percent-threshold", "20"])
            self.assertEqual(code, 0)
            self.assertIn("Revenue", output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
