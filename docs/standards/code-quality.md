# Code Quality Baseline

This repository starts with a lightweight, language-agnostic quality standard.

## Standards

- Use `.editorconfig` defaults for consistent formatting.
- Keep commits small and focused.
- Run `pre-commit run --all-files` before pushing.
- Prefer clear naming and short functions.
- Add tests for behavior changes when implementation begins.

## Required Local Checks

```bash
pre-commit run --all-files
```

## CI Enforcement

GitHub Actions runs the same pre-commit checks in `.github/workflows/quality-and-secrets.yml`.
