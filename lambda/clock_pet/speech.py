"""SSML helpers for Mascota."""

from clock_pet.constants import BLINK_SFX


def build_blink_ssml(message: str = "blink") -> str:
    """Create compact SSML speech for interaction events."""
    return f"<speak><audio src=\"{BLINK_SFX}\"/>{message}</speak>"
