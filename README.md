# AI Pioneer

AI Pioneer is a small, deterministic financial variance review tool for Korean
students and accounting or finance practitioners. It turns a simple CSV into a
review-ready Markdown report without uploading financial data to a third party.

The project is intentionally narrow: it provides an inspectable baseline that
can later support documented AI-assisted explanations, issue triage, and
maintainer automation.

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
