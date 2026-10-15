# AI Pioneer

AI Pioneer is a small, deterministic financial variance review tool for Korean
students and accounting or finance practitioners. It turns a simple CSV into a
review-ready Markdown report without uploading financial data to a third party.

The project is intentionally narrow: it provides an inspectable baseline that
can later support documented AI-assisted explanations, issue triage, and
maintainer automation.

## 잔액브릿지 v0.1.0 · 유료 편의 패키지

잔액브릿지는 로컬 Chrome에서 두 CSV 파일의 잔액을 비교하는 다운로드형 ZIP 패키지입니다.

- 파일별 열 매핑, 누락·중복·기준 잔액 0 예외 확인
- 비교 결과 CSV와 한국어 요약 다운로드
- XLSX 직접 입력은 지원하지 않으며, 회계적 판단을 대신하지 않습니다.

이 저장소의 AI Pioneer는 MIT 라이선스로 공개된 오픈소스 프로젝트입니다.
잔액브릿지는 별도로 구매할 수 있는 편의 패키지이며, 기존 프로젝트의 MIT 라이선스는 그대로 유지됩니다.

[상품 소개 및 구매하기](https://balancebridgetools.gumroad.com/l/cwecgs) · 19,000원 · 일회성 구매

## Project identity and contact

- **Project:** AI Pioneer, maintained by 신대환 (Daehwan Shin),
  [@noenemysogang](https://github.com/noenemysogang).
- **Website and working example:** https://www.aipioneer-dh.dynv6.net/
- **Project email:** [hello@aipioneer-dh.dynv6.net](mailto:hello@aipioneer-dh.dynv6.net).
- **Public development evidence:** [commit history](https://github.com/noenemysogang/DH/commits/main/),
  [test source](test_ai_pioneer.py), and [CI results](https://github.com/noenemysogang/DH/actions).

This repository is the source for the project website. AI Pioneer is a
pre-release project; Claude integration is planned and is not yet implemented.
Repository dates describe development history, not a company's legal incorporation.

## What it does

- Reads UTF-8 CSV files with `account`, `current`, and `prior` columns.
- Flags changes that exceed both percentage and amount thresholds.
- Handles comma-separated amounts and accounting negatives such as `(250)`.
- Treats a new nonzero balance with a zero prior balance as a flagged variance.
- Produces Korean or English Markdown output.
- Uses only the Python standard library.

## Quick start

Python 3.10 or newer is required.

```bash
git clone https://github.com/noenemysogang/DH.git
cd DH
python ai_pioneer.py sample_financials.csv -o report.md
```

Choose explicit review thresholds:

```bash
python ai_pioneer.py sample_financials.csv \
  --percent-threshold 20 \
  --amount-threshold 1000000 \
  --locale ko \
  --top 10 \
  -o report.md
```

The thresholds are screening rules, not audit conclusions. Reviewers remain
responsible for source-data completeness, materiality, and professional
judgment.

## Input format

```csv
account,current,prior
Revenue,125000000,100000000
Operating expenses,78000000,60000000
Cash,42000000,50000000
```

Amounts must use the same currency and unit throughout a file. The tool does
not infer exchange rates or accounting standards.

## Test

```bash
python -m unittest -v
```

## Roadmap

- Publish versioned releases and packaged installation.
- Add documented, opt-in AI explanations with redaction and cost controls.
- Add reproducible evaluation fixtures for Korean financial terminology.
- Automate issue triage, pull-request review, and release notes.
- Gather real user feedback before expanding the data model.

## Project status

AI Pioneer is pre-release. It currently has no external adoption claims. The
repository is being developed in public so that design choices, tests, and
limitations remain inspectable.

## Contributing and security

See [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution workflow and
[SECURITY.md](SECURITY.md) for private vulnerability reporting guidance.

## License

MIT. See [LICENSE](LICENSE).
