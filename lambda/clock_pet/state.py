"""Session state helpers for Mascota."""

from clock_pet.constants import DEFAULT_EYE_INDEX, DEFAULT_MOOD, EYE_FRAMES, VALID_MOODS


def normalize_state(session_attributes: dict | None) -> dict:
    """Return normalized v1 state from possibly-invalid session attributes."""
    attributes = session_attributes or {}

    eye_index = attributes.get("eyeIndex", DEFAULT_EYE_INDEX)
    mood = attributes.get("mood", DEFAULT_MOOD)

    if not isinstance(eye_index, int):
        eye_index = DEFAULT_EYE_INDEX
    if eye_index < 0 or eye_index >= len(EYE_FRAMES):
        eye_index = DEFAULT_EYE_INDEX

    if mood not in VALID_MOODS:
        mood = DEFAULT_MOOD

    return {"eyeIndex": eye_index, "mood": mood}


def advance_eye_index(current_eye_index: int) -> int:
    """Advance and wrap eye index within known frames."""
    return (current_eye_index + 1) % len(EYE_FRAMES)


def next_state(session_attributes: dict | None) -> tuple[dict, str]:
    """Compute next state and selected frame for response rendering."""
    state = normalize_state(session_attributes)
    new_eye_index = advance_eye_index(state["eyeIndex"])
    frame = EYE_FRAMES[new_eye_index]

    return {"eyeIndex": new_eye_index, "mood": state["mood"]}, frame
