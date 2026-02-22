# Python-First v1 Implementation Plan (Mascota)

This plan defines a practical v1 for building **Mascota** with a Python-based Alexa backend, optimized for fast iteration and safe growth.

## 1) Why Python-first

Choose Python as the primary implementation language because:

- Faster development velocity for the current owner/team.
- Logic is event-driven and lightweight; Python runtime is fully suitable.
- Easy progression from session-only state to DynamoDB-backed persistence.

## 2) v1 Scope (what to build now)

### In scope

- Invocation + launch behavior (`LaunchRequest`).
- One interaction intent (e.g., `BlinkIntent` or `PetIntent`).
- Eye-frame progression per request using session attributes.
- APL-T render directive for 4-character display output.
- Short SSML response with blink sound + pet phrase.
- Basic fallback/help/cancel handlers.

### Out of scope (v2+)

- Long-term memory persistence.
- Timed mood decay.
- Advanced randomized behavior.
- Multiple locales.

## 3) Proposed repository structure

```text
clock-pet/
├── lambda/
│   ├── handler.py
│   ├── requirements.txt
│   ├── apl/
│   │   └── eyes.aplt.json
│   └── clock_pet/
│       ├── __init__.py
│       ├── constants.py
│       ├── state.py
│       ├── renderer.py
│       ├── speech.py
│       └── handlers/
│           ├── __init__.py
│           ├── launch.py
│           ├── interaction.py
│           ├── help.py
│           ├── cancel.py
│           └── fallback.py
├── tests/
│   ├── test_state.py
│   └── test_renderer.py
└── docs/
    └── design/
        └── clock-pet.md
```

## 4) Component responsibilities

- `handler.py`: Alexa SDK entrypoint, registration of request handlers.
- `constants.py`: eye frames, mood enums, soundbank constants, limits.
- `state.py`: session state transitions (`eyeIndex`, `mood`).
- `renderer.py`: builds APL-T directive payload.
- `speech.py`: short voice lines + SSML assembly.
- `handlers/*`: thin routing logic; delegate business logic to modules.

## 5) Data model (v1)

Session attributes only:

- `eyeIndex: int` (default `0`)
- `mood: str` (`awake` default)

Rules:

- `eyeIndex = (eyeIndex + 1) % len(EYE_FRAMES)` on each handled interaction.
- Eye frame output must be <= 4 display characters.
- All unsupported state values fall back to defaults.

## 6) Request flow (v1)

For launch/interaction:

1. Read session attributes.
2. Normalize state.
3. Compute next eye frame.
4. Build APL-T document with selected frame.
5. Build SSML response (optional blink sound + phrase).
6. Return response + `Alexa.Presentation.APL.RenderDocument` directive.

## 7) Deployment strategy

### Phase A (recommended first): Alexa-hosted (Python)

- Fastest setup and iteration for v1.
- Use Alexa Developer Console simulator to validate behavior.
- Keep dependencies minimal to reduce packaging complexity.

#### Copy/paste click path checklist (your case)

Use this when you want the quickest path from zero to simulator test.

1. Open **Alexa Developer Console** → **Create Skill**.
2. Enter:
   - **Skill name**: `Mascota`
   - **Primary locale**: `Spanish (ES)`
   - **Model**: `Custom`
   - **Hosting service**: `Alexa-hosted (Python)`
3. Click **Create skill**.
4. Go to **Build** tab:
   - In left nav, open **Interfaces**.
   - Enable **Alexa Presentation Language (APL)**.
   - Save model.
5. Still in **Build** tab:
   - Open **Invocation**.
   - Set invocation name to `levanta mascota` (minimum 2 words).
   - Save model.
6. In left nav, select **Interaction Model** → **Build Model**.
7. Go to **Code** tab:
   - Confirm runtime is Python for Alexa-hosted skill.
   - Paste/update handler code for launch + interaction + help/cancel/fallback.
   - Save and deploy from the hosted editor.
8. Go to **Test** tab:
   - Toggle testing to **Development**.
   - Select device profile **Echo Dot with Clock**.
   - Type/say: `abre levanta mascota`.
9. Repeat invocation 5-10 times and verify:
   - eye frame progresses each interaction,
   - displayed frame is <= 4 characters,
   - help/fallback remain short and stable.
10. Local quality gate before sharing changes:
    - Run `pre-commit run --all-files`.


#### What to preserve in your local Alexa-hosted repo

If your local project looks like:

- `lambda/`
- `skill-package/`
- `ask-resources.json`
- `Mascota.code-workspace`

Preserve these as follows:

1. **Keep `lambda/`** (required):
   - contains runtime code and assets used by Alexa-hosted deployment.
2. **Keep `skill-package/`** (required):
   - contains interaction model(s), responses, and skill manifest (`skill.json`).
3. **Keep `ask-resources.json`** (required for ASK CLI sync/deploy):
   - links your local repo/profile to the hosted skill id and infra type.
4. **Keep `Mascota.code-workspace`** (optional, local-only):
   - editor convenience file; safe to keep in repo or ignore by team preference.

Safe defaults when syncing this repo to your CodeCommit remote:

- If using full-repo sync, commit/push: `lambda/`, `skill-package/`, `ask-resources.json`, docs/scripts.
- If using `scripts/sync_repo.sh`, only `lambda/` is synced to destination; target `skill-package/` and `ask-resources.json` stay as-is.
- Do **not** commit credentials/secrets (none should be stored in these files).
- If you use local-only IDE settings, optionally add workspace file to `.gitignore` in your personal fork.

### Phase B (optional): AWS Lambda-managed

Move when you need stronger infra controls:

- Centralized IAM and environment management.
- Deeper CloudWatch observability and deployment automation.
- Clearer multi-environment promotion workflows.

## 8) Test strategy

### Local unit tests

- `test_state.py`
  - advances eye index correctly
  - wraps index correctly
  - handles missing/invalid session values
- `test_renderer.py`
  - emits valid directive shape
  - includes APL-T `Text` item with <= 4 characters

### Console/simulator tests

- Device profile: Echo Dot with Clock.
- Voice test phrase: `abre levanta mascota`.
- Repeat invocation 5-10 times and verify frame progression.
- Validate help/fallback responses are short and stable.

### Quality/secrets checks

- `pre-commit run --all-files`
- Ensure no credentials in code or docs.

## 9) Milestones

### Milestone 1 — skeleton (0.5 day)

- create Python package layout
- implement launch + help + cancel handlers
- render static eye frame

### Milestone 2 — interaction loop (0.5-1 day)

- implement state transitions
- add interaction intent
- add blink SSML + frame progression

### Milestone 3 — hardening (0.5 day)

- add fallback/error behavior
- add unit tests for state/renderer
- run quality + secrets checks

## 10) Definition of Done (v1)

- Skill launches in simulator and renders valid 4-char eye output.
- At least one interaction advances the frame and responds with SSML.
- Help/cancel/fallback handlers work.
- Unit tests for state + renderer pass locally.
- Repository quality/secrets checks pass.
