"""LaunchRequest handler."""

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_request_type

from clock_pet.constants import EYE_FRAMES
from clock_pet.renderer import build_aplt_render_directive


class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input: HandlerInput):
        frame = EYE_FRAMES[0]
        directive = build_aplt_render_directive(frame)
        handler_input.attributes_manager.session_attributes.update({"eyeIndex": 0, "mood": "awake"})

        return (
            handler_input.response_builder.speak("<speak>Hello, I am Clock Pet.</speak>")
            .add_directive(directive)
            .set_should_end_session(False)
            .response
        )
