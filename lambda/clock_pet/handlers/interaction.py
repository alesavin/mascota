"""PetIntent interaction handler."""

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_intent_name

from clock_pet.i18n import message
from clock_pet.renderer import build_render_directive_for_device, device_supports_apl
from clock_pet.speech import build_blink_ssml
from clock_pet.state import next_state


class PetIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_intent_name("PetIntent")(handler_input)

    def handle(self, handler_input: HandlerInput):
        session_attributes = handler_input.attributes_manager.session_attributes
        new_state, frame = next_state(session_attributes)
        session_attributes.update(new_state)

        locale = handler_input.request_envelope.request.locale
        response_builder = handler_input.response_builder.speak(
            build_blink_ssml(message(locale, "pet"))
        )

        if device_supports_apl(handler_input):
            directive = build_render_directive_for_device(handler_input, frame)
            if directive is not None:
                response_builder.add_directive(directive)

        return response_builder.set_should_end_session(False).response
