"""Render APL-T directives for Mascota."""


def build_aplt_render_directive(frame: str) -> dict:
    """Build a minimal APL-T render directive for a 4-character display."""
    safe_frame = frame[:4]

    return {
        "type": "Alexa.Presentation.APL.RenderDocument",
        "token": "clockPetEyes",
        "document": {
            "type": "APL",
            "version": "1.8",
            "theme": "dark",
            "mainTemplate": {
                "parameters": ["payload"],
                "items": [
                    {
                        "type": "Text",
                        "text": safe_frame,
                        "fontSize": "42dp",
                        "textAlign": "center",
                        "textAlignVertical": "center",
                        "width": "100vw",
                        "height": "100vh",
                    }
                ],
            },
        },
        "datasources": {},
    }
