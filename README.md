# Mascota

This repository is prepared with a quality and secrets baseline so project implementation can start safely.

## What's included

- Code quality guardrails (EditorConfig + pre-commit checks).
- Secrets-scanning baseline (`gitleaks` config + pre-commit hook).
- CI workflow to enforce standards on pull requests.
- Product design notes for **Mascota** in `docs/design/clock-pet.md`.

## Quick start

1. Install pre-commit:
   ```bash
   pip install pre-commit
   ```
2. Install hooks:
   ```bash
   pre-commit install
   ```
3. Run all checks locally:
   ```bash
   pre-commit run --all-files
   ```
