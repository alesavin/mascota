"""Lambda entrypoint for Mascota Alexa skill."""

from ask_sdk_core.skill_builder import SkillBuilder

from clock_pet.handlers.cancel import CancelOrStopIntentHandler
from clock_pet.handlers.fallback import FallbackIntentHandler
from clock_pet.handlers.help import HelpIntentHandler
from clock_pet.handlers.interaction import PetIntentHandler
from clock_pet.handlers.launch import LaunchRequestHandler
from clock_pet.handlers.unhandled import SessionEndedRequestHandler, UnhandledRequestHandler

sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(PetIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(UnhandledRequestHandler())

lambda_handler = sb.lambda_handler()
