# 👀 Mascota — “Fake Eyes” Alexa Skill (Echo Dot with Clock)

A minimal Alexa Skill that renders fake animated “eyes” on Echo Dot with Clock using APL-T (character display).

This project creates the illusion of animation through interaction rhythm:

User speaks → Blink sound → Eye frame changes → Pet speaks.

The device is event-driven only, so animation is simulated by switching eye frames per interaction.

## 🎯 Target Device

- Echo Dot with Clock
- 4-character LED display
- Character-based rendering only (APL-T)
- No pixel graphics
- No real animation support

## 🧠 Concept

The pet has simple state:

- `mood`: `awake | sleepy | excited`
- `eyeFrame`: string (max 4 characters)
- optional session memory

Each interaction:

1. Update state
2. Select next eye frame
3. Play short blink sound
4. Render new APL-T text
5. Speak short pet response

## 🏗 Architecture

### Alexa APIs Used

- `LaunchRequest`
- Custom intents (optional)
- `Alexa.Presentation.APL.RenderDocument`
- SSML audio output
- Session attributes (initial state storage)
- Optional: DynamoDB persistence (later)

## 🖥 Development Setup

### Recommended Workflow

- Source control: GitHub
- Development: ChatGPT Codex
- Deployment: Alexa Developer Console
- Hosting:
  - Option A: Alexa-hosted (fastest iteration)
  - Option B: AWS Lambda (Node.js or Python)

## 📂 Suggested Repo Structure

```text
clock-pet/
│
├── lambda/                # or /src
│   ├── handler.js         # Node version
│   ├── handler.py         # Python version (optional alternative)
│   └── apl/
│       └── eyes.aplt.json
│
├── skill.json             # optional skill manifest
└── README.md
```

## 👀 APL-T Document (Minimal Example)

**File:** `lambda/apl/eyes.aplt.json`

```json
{
  "type": "APLT",
  "version": "1.0",
  "mainTemplate": {
    "items": [
      {
        "type": "Text",
        "text": "0 0"
      }
    ]
  }
}
```

## 🔊 Interaction Rhythm (Fake Animation Pattern)

Example blink cycle:

| Step | Eyes | Audio | Speech |
|---|---|---|---|
| 1 | `0 0` | blink | “I’m awake!” |
| 2 | `--__` | blink | “blink” |
| 3 | `0 0` | none | “Hi again.” |

Each request advances the frame.
No background timers.
No loops.
No continuous rendering.

## 🟢 Node.js Minimal Handler Skeleton

**File:** `lambda/handler.js`

```js
const Alexa = require('ask-sdk-core');

const EYE_FRAMES = ["0 0", "--__", "8.8"];

const LaunchRequestHandler = {
  canHandle(handlerInput) {
    return Alexa.getRequestType(handlerInput.requestEnvelope) === 'LaunchRequest';
  },
  handle(handlerInput) {

    const session = handlerInput.attributesManager.getSessionAttributes();
    const index = (session.eyeIndex || 0) % EYE_FRAMES.length;

    session.eyeIndex = index + 1;
    handlerInput.attributesManager.setSessionAttributes(session);

    const aplDoc = {
      type: 'APLT',
      version: '1.0',
      mainTemplate: {
        items: [
          { type: 'Text', text: EYE_FRAMES[index] }
        ]
      }
    };

    return handlerInput.responseBuilder
      .speak('<audio src="soundbank://soundlibrary/ui/gameshow/amzn_ui_sfx_gameshow_tally_positive_01"/> Hi!')
      .addDirective({
        type: 'Alexa.Presentation.APL.RenderDocument',
        document: aplDoc
      })
      .getResponse();
  }
};

exports.handler = Alexa.SkillBuilders.custom()
  .addRequestHandlers(LaunchRequestHandler)
  .lambda();
```

## 🐍 Python Minimal Handler Skeleton

**File:** `lambda/handler.py`

```python
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type

EYE_FRAMES = ["0 0", "--__", "8.8"]

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        session = handler_input.attributes_manager.session_attributes
        index = session.get("eyeIndex", 0) % len(EYE_FRAMES)

        session["eyeIndex"] = index + 1

        apl_doc = {
            "type": "APLT",
            "version": "1.0",
            "mainTemplate": {
                "items": [
                    {"type": "Text", "text": EYE_FRAMES[index]}
                ]
            }
        }

        handler_input.response_builder.speak(
            '<audio src="soundbank://soundlibrary/ui/gameshow/amzn_ui_sfx_gameshow_tally_positive_01"/> Hi!'
        ).add_directive({
            "type": "Alexa.Presentation.APL.RenderDocument",
            "document": apl_doc
        })

        return handler_input.response_builder.response

sb = SkillBuilder()
sb.add_request_handler(LaunchRequestHandler())

lambda_handler = sb.lambda_handler()
```

## 🚀 How to Test

1. Create Alexa Skill (Custom)
2. Enable APL interface
3. Deploy (Alexa-hosted or Lambda)
4. Open Simulator
5. Select device: Echo Dot with Clock
6. Say: `open mascota`

## 📌 Design Rules

- Keep eye frames ≤ 4 characters
- Avoid unsupported characters
- No APL layouts (APLT only)
- No animations (simulate with state changes)
- Keep interaction short and expressive

## 🧩 Future Enhancements

- Add moods
- Add feeding / petting intents
- Add persistent memory (DynamoDB)
- Add timed mood decay
- Add randomized blink pattern

## 🧠 Development Philosophy

This project embraces constraints:

- Limited display
- Event-driven model
- No true animation

The “life” of the pet comes from:

- Rhythm
- Sound design
- Small state transitions


## Localization

The runtime speech layer supports language-specific messaging by reading `request.locale` and mapping it to language codes.
Current mappings include:
- `en-*`: launch cue `mrrr`, prompt `wake up, mascota`
- `es-*`: launch cue `mrrr`, prompt `coge, mascota`

To add another language, extend `lambda/clock_pet/i18n.py` with a new language entry.
