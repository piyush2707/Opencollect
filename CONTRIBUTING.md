# Contributing to OpenCollect

Thanks for considering a contribution!

## Before you start

- Search existing issues to avoid duplicates.
- For large changes, open an issue first to discuss the proposed design.
- Keep pull requests focused and small.
- Never commit real customer data, API keys, passwords, or other secrets.

## Development setup

OpenCollect's initial core uses only the Python standard library.

```bash
python -m unittest discover -s tests -v
```

## Pull request checklist

- [ ] The change solves one clear problem.
- [ ] Tests were added or updated where appropriate.
- [ ] Documentation was updated.
- [ ] No secrets or real customer financial data were added.
- [ ] User-facing messages remain respectful and factual.

## Good first contributions

- Add more CSV validation tests.
- Improve error messages.
- Add editable reminder templates.
- Add Hindi and English template examples.
- Improve the README with tested examples.

## Code style

Use clear names, type hints for public functions, and standard-library dependencies where practical. Keep core invoice logic separate from API or AI provider code.
