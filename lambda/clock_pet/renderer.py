"""Render APL/APL-T directives for Mascota."""

from typing import Optional

from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import get_supported_interfaces
from ask_sdk_model.interfaces.alexa.presentation.apl import (
    RenderDocumentDirective as AplRenderDocumentDirective,
)
from ask_sdk_model.interfaces.alexa.presentation.aplt import (
    RenderDocumentDirective as ApltRenderDocumentDirective,
)


def _get_supported_interfaces(handler_input: HandlerInput):
    """Safely return the device supported interfaces object."""
    try:
        return get_supported_interfaces(handler_input)
    except AttributeError:
        return None


def device_supports_apl(handler_input: HandlerInput) -> bool:
    """Return whether the current device can render APL or APL-T directives."""
    supported_interfaces = _get_supported_interfaces(handler_input)
    if not supported_interfaces:
        return False

    return bool(
        getattr(supported_interfaces, "alexa_presentation_aplt", None)
        or getattr(supported_interfaces, "alexa_presentation_apl", None)
    )


def build_render_directive_for_device(
    handler_input: HandlerInput, frame: str
) -> Optional[object]:
    """Build a render directive matching the device capabilities."""
    supported_interfaces = _get_supported_interfaces(handler_input)
    if not supported_interfaces:
        return None

    safe_frame = frame[:4]
    document_type = "APLT"

    if getattr(supported_interfaces, "alexa_presentation_aplt", None):
        return ApltRenderDocumentDirective(
            token="clockPetEyes",
            document={
                "type": document_type,
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
            datasources={},
        )

    if getattr(supported_interfaces, "alexa_presentation_apl", None):
        return AplRenderDocumentDirective(
            token="clockPetEyes",
            document={
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
            datasources={},
        )

    return None
