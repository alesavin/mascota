import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "lambda"))

from clock_pet.i18n import message


def test_english_messages_are_used_for_en_locale():
    assert message("en-US", "help") == "Say wake up, mascota."


def test_spanish_messages_are_used_for_es_locale():
    assert message("es-ES", "help") == "Di coge, mascota."


def test_unsupported_locales_fall_back_to_english():
    assert message("fr-FR", "launch") == "mrrr"
    assert message("fr-FR", "goodbye") == "Goodbye."
