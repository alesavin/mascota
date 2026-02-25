import pathlib
import sys
from types import SimpleNamespace

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "lambda"))

from ask_sdk_model.interfaces.alexa.presentation.apl import AlexaPresentationAplInterface
from ask_sdk_model.interfaces.alexa.presentation.aplt import AlexaPresentationApltInterface
from ask_sdk_model.supported_interfaces import SupportedInterfaces

from clock_pet.renderer import build_render_directive_for_device, device_supports_apl


def _handler_input_with_interfaces(supported_interfaces):
    return SimpleNamespace(
        request_envelope=SimpleNamespace(
            context=SimpleNamespace(
                system=SimpleNamespace(
                    device=SimpleNamespace(supported_interfaces=supported_interfaces)
                )
            )
        )
    )


def test_returns_aplt_directive_for_echo_dot_with_clock_profile():
    handler_input = _handler_input_with_interfaces(
        SupportedInterfaces(alexa_presentation_aplt=AlexaPresentationApltInterface())
    )

    directive = build_render_directive_for_device(handler_input, "o_o")

    assert directive is not None
    assert directive.object_type == "Alexa.Presentation.APLT.RenderDocument"
    assert directive.document["type"] == "APLT"


def test_returns_apl_directive_for_alexa_app_profile():
    handler_input = _handler_input_with_interfaces(
        SupportedInterfaces(alexa_presentation_apl=AlexaPresentationAplInterface())
    )

    directive = build_render_directive_for_device(handler_input, "o_o")

    assert directive is not None
    assert directive.object_type == "Alexa.Presentation.APL.RenderDocument"
    assert directive.document["type"] == "APL"


def test_returns_none_when_device_has_no_presentation_interface():
    handler_input = _handler_input_with_interfaces(SupportedInterfaces())

    assert device_supports_apl(handler_input) is False
    assert build_render_directive_for_device(handler_input, "o_o") is None


def test_frame_is_capped_to_four_characters():
    handler_input = _handler_input_with_interfaces(
        SupportedInterfaces(alexa_presentation_aplt=AlexaPresentationApltInterface())
    )

    directive = build_render_directive_for_device(handler_input, "12345")
    rendered_frame = directive.document["mainTemplate"]["items"][0]["text"]

    assert len(rendered_frame) <= 4
