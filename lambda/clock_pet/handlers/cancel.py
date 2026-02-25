"""Cancel and Stop handlers."""

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_intent_name

from clock_pet.i18n import message


class CancelOrStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_intent_name("AMAZON.CancelIntent")(handler_input) or is_intent_name("AMAZON.StopIntent")(
            handler_input
        )

    def handle(self, handler_input: HandlerInput):
        locale = handler_input.request_envelope.request.locale
        return handler_input.response_builder.speak(message(locale, "goodbye")).set_should_end_session(True).response
