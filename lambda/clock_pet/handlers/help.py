"""AMAZON.HelpIntent handler."""

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_intent_name

from clock_pet.i18n import message


class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input: HandlerInput):
        locale = handler_input.request_envelope.request.locale
        prompt = message(locale, "help")
        return handler_input.response_builder.speak(prompt).ask(prompt).response
