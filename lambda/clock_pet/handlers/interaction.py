"""PetIntent interaction handler."""

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_intent_name

from clock_pet.renderer import build_aplt_render_directive
from clock_pet.speech import build_blink_ssml
from clock_pet.state import next_state


class PetIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_intent_name("PetIntent")(handler_input)

    def handle(self, handler_input: HandlerInput):
        session_attributes = handler_input.attributes_manager.session_attributes
        new_state, frame = next_state(session_attributes)
        session_attributes.update(new_state)

        directive = build_aplt_render_directive(frame)
        return (
            handler_input.response_builder.speak(build_blink_ssml("good pet"))
            .add_directive(directive)
            .set_should_end_session(False)
            .response
        )
