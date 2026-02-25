"""Localization helpers for Mascota speech text."""

from __future__ import annotations

DEFAULT_LOCALE = "en"

MESSAGES = {
    "en": {
        "launch": "mrrr",
        "help": "Say wake up, mascota.",
        "fallback": "I only understand wake up, mascota right now.",
        "fallback_reprompt": "Say wake up, mascota.",
        "pet": "good pet",
        "goodbye": "Goodbye.",
    },
    "es": {
        "launch": "mrrr",
        "help": "Di coge, mascota.",
        "fallback": "Por ahora solo entiendo coge, mascota.",
        "fallback_reprompt": "Di coge, mascota.",
        "pet": "buen mascota",
        "goodbye": "Adiós.",
    },
}


def _language_code(locale: str | None) -> str:
    if not locale:
        return DEFAULT_LOCALE
    return locale.split("-")[0].lower()


def message(locale: str | None, key: str) -> str:
    language = _language_code(locale)
    language_messages = MESSAGES.get(language, MESSAGES[DEFAULT_LOCALE])
    return language_messages.get(key, MESSAGES[DEFAULT_LOCALE][key])
