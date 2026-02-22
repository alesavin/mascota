"""Handlers for unexpected request types."""

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_request_type


class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input: HandlerInput):
        return handler_input.response_builder.response


class UnhandledRequestHandler(AbstractRequestHandler):
    """Fallback request handler that prevents dispatch errors."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return True

    def handle(self, handler_input: HandlerInput):
        return (
            handler_input.response_builder.speak("Sorry, I couldn't process that request.")
            .set_should_end_session(True)
            .response
        )
