"""LaunchRequest handler."""

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_request_type

from clock_pet.constants import EYE_FRAMES
from clock_pet.i18n import message
from clock_pet.renderer import build_render_directive_for_device, device_supports_apl


class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input: HandlerInput):
        frame = EYE_FRAMES[0]
        handler_input.attributes_manager.session_attributes.update({"eyeIndex": 0, "mood": "awake"})

        locale = handler_input.request_envelope.request.locale
        launch_speech = message(locale, "launch")
        response_builder = handler_input.response_builder.speak(f"<speak>{launch_speech}</speak>")

        if device_supports_apl(handler_input):
            directive = build_render_directive_for_device(handler_input, frame)
            if directive is not None:
                response_builder.add_directive(directive)

        return response_builder.set_should_end_session(False).response
