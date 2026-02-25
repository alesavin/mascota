import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "lambda"))

from clock_pet.constants import BLINK_SFX
from clock_pet.speech import build_blink_ssml


def test_build_blink_ssml_uses_configured_soundbank_asset():
    ssml = build_blink_ssml("hola")
    assert ssml == f'<speak><audio src="{BLINK_SFX}"/>hola</speak>'
    assert "soundbank://soundlibrary/ui/gameshow/" in ssml
