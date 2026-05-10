# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**Run tests:**
```bash
pytest -q
```

**Run a single test file:**
```bash
pytest tests/test_state.py -q
```

**Run pre-commit checks (linting, formatting, secrets scanning):**
```bash
pre-commit run --all-files
```

## Architecture

Mascota is an Alexa skill for the Echo Dot with Clock that renders animated "eyes" on the 4-character LED display. Written in Python, deployed as an AWS Lambda function using the ASK SDK.

**Request flow:** User speaks → Alexa routes intent → Handler updates session state → Renderer builds APL-T directive → Speech module builds SSML → Response sent back.

### Key modules (`lambda/clock_pet/`)

| Module | Role |
|--------|------|
| `constants.py` | `EYE_FRAMES`, mood names, sound effect paths |
| `state.py` | Normalizes and advances eye frame index across interactions |
| `renderer.py` | Builds APL/APL-T directives; detects device type (`alexa_presentation_aplt` for Echo Dot with Clock, falls back to `alexa_presentation_apl`) |
| `speech.py` | Generates SSML with blink sound effects |
| `i18n.py` | Localized strings for `en-US` and `es-ES` |
| `handlers/` | One file per Alexa intent (launch, interaction/PetIntent, help, fallback, cancel, unhandled) |

**Entry point:** `lambda/lambda_function.py` → `lambda/handler.py` (SkillBuilder setup and request routing)

**Interaction model:** `skill-package/interactionModels/custom/` — Alexa intent schemas for `en-US` and `es-ES`. The `PetIntent` must be defined manually in the Alexa Console or via ASK CLI before the skill is functional.

**Tests:** `tests/` covers state cycling (`test_state.py`), rendering (`test_renderer.py`), i18n (`test_i18n.py`), and speech generation (`test_speech.py`).

**Python version:** 3.8 (AWS Lambda runtime). Only dependency: `ask-sdk-core >= 1.19.0`.
