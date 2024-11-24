# from ducklingscript import
from ducklingscript import DucklingCompiler, InvalidArgumentsError
import pytest


def test_basic_alt():
    x = DucklingCompiler().compile(["alt a", "alt B"], skip_indentation=True)
    assert x.output == ["ALT a", "ALT B"]


def test_adv_alt_1():
    x = DucklingCompiler().compile(["alt f1", "aLt esc"], skip_indentation=True)
    assert x.output == ["ALT F1", "ALT ESC"]


def test_alt_err():
    with pytest.raises(InvalidArgumentsError):
        DucklingCompiler().compile(["alt ab"])
