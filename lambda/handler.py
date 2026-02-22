"""Lambda entrypoint for Clock Pet Alexa skill."""

from ask_sdk_core.skill_builder import SkillBuilder

from clock_pet.handlers.cancel import CancelOrStopIntentHandler
from clock_pet.handlers.fallback import FallbackIntentHandler
from clock_pet.handlers.help import HelpIntentHandler
from clock_pet.handlers.interaction import PetIntentHandler
from clock_pet.handlers.launch import LaunchRequestHandler

sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(PetIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())

lambda_handler = sb.lambda_handler()
