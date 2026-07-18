# Contributing

Thank you for helping improve AI Pioneer.

## Before opening a change

1. Search existing issues and pull requests.
2. Open an issue for behavior changes or new data formats.
3. Do not include confidential financial data, credentials, or personal data.

## Development

```bash
python -m unittest -v
python ai_pioneer.py sample_financials.csv --locale en
```

Keep the deterministic analysis path dependency-free. New behavior should
include tests for valid input, invalid input, and threshold boundaries.

## Pull requests

- Keep each pull request focused.
- Explain the accounting or reviewer workflow being improved.
- Document user-visible behavior and limitations.
- Confirm that tests pass on a supported Python version.

By contributing, you agree that your contribution is licensed under the MIT
License.
