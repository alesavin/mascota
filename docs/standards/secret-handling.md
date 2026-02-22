# Secrets Handling Baseline

## Rules

- Never commit real credentials, API keys, private keys, or tokens.
- Keep local secrets in `.env` files (ignored by `.gitignore`).
- Use environment variables or managed secrets at runtime.
- Rotate any secret immediately if exposed.

## Automated Protection

- `detect-private-key` hook blocks committing private keys.
- `gitleaks` scans staged/all files for high-risk patterns.
- CI re-runs scans on every pull request.

## Incident Response (minimum)

1. Revoke/rotate leaked secret.
2. Remove secret from repository history if needed.
3. Add or tighten detection rule to prevent recurrence.
