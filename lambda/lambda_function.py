"""Compatibility AWS Lambda entrypoint.

Alexa-hosted and ASK CLI deployments default to ``lambda_function.lambda_handler``.
This module forwards that handler to the project's main implementation in
``handler.py``.
"""

from handler import lambda_handler
