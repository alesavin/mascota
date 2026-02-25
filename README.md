# Mascota

This repository is prepared with a quality and secrets baseline so project implementation can start safely.

## What's included

- Code quality guardrails (EditorConfig + pre-commit checks).
- Secrets-scanning baseline (`gitleaks` config + pre-commit hook).
- CI workflow to enforce standards on pull requests.
- Product design notes for **Mascota** in `docs/design/clock-pet.md`.
- Alexa interaction model starters with `PetIntent` in:
  - `skill-package/interactionModels/custom/en-US.json`
  - `skill-package/interactionModels/custom/es-ES.json`

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

## Define `PetIntent` (Console or JSON file)

`lambda/clock_pet/handlers/interaction.py` expects a custom intent named `PetIntent`.

### Option A: Alexa Developer Console (UI)

1. Open your skill at <https://developer.amazon.com/alexa/console/ask>.
2. Go to **Build** → **Interaction Model** → **Intents**.
3. Click **Add Intent**.
4. Enter intent name: `PetIntent`.
5. Add sample utterances, for example:
   - `pet`
   - `pet mascota`
   - `wake up mascota` (matches current help/fallback guidance)
   - `pat`
   - `show eyes`
6. Save model and click **Build Model**.

### Option B: By file (recommended)

1. Use the checked-in model file for your locale:
   - English (US): `skill-package/interactionModels/custom/en-US.json`
   - Spanish (ES): `skill-package/interactionModels/custom/es-ES.json`
2. In Alexa Console, open **JSON Editor** under **Interaction Model**.
3. Paste the locale file content (or merge `PetIntent` into your existing model).
4. Save and **Build Model**.

If you use SMAPI/ASK CLI later, this same file can be deployed as part of your skill package.
