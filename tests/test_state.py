import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "lambda"))

from clock_pet.state import advance_eye_index, next_state, normalize_state


def test_advances_eye_index():
    assert advance_eye_index(0) == 1


def test_wraps_eye_index():
    assert advance_eye_index(3) == 0


def test_normalize_with_missing_and_invalid_values():
    assert normalize_state(None) == {"eyeIndex": 0, "mood": "awake"}
    assert normalize_state({"eyeIndex": "x", "mood": "unknown"}) == {"eyeIndex": 0, "mood": "awake"}


def test_next_state_returns_frame_for_next_index():
    state, frame = next_state({"eyeIndex": 0, "mood": "awake"})
    assert state["eyeIndex"] == 1
    assert frame == "-_-"
