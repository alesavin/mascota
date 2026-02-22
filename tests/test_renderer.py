import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "lambda"))

from clock_pet.renderer import build_aplt_render_directive


def test_emits_valid_directive_shape():
    directive = build_aplt_render_directive("o_o")
    assert directive.object_type == "Alexa.Presentation.APL.RenderDocument"
    assert directive.document["mainTemplate"]["items"][0]["type"] == "Text"


def test_frame_is_capped_to_four_characters():
    directive = build_aplt_render_directive("12345")
    rendered_frame = directive.document["mainTemplate"]["items"][0]["text"]
    assert len(rendered_frame) <= 4
