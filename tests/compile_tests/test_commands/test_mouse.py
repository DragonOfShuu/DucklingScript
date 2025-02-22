from ducklingscript import DucklingCompiler
from pytest import raises

from ducklingscript import InvalidArgumentsError

def test_mouse_click():
    x = ["rightclick"]
    answer = DucklingCompiler().compile(x, skip_indentation=True)
    assert answer.output == ["RIGHTCLICK"]

def test_mouse_move():
    x = ["MOUSEMOVE"]
    with raises(InvalidArgumentsError):
        DucklingCompiler().compile(x, skip_indentation=True)

    x = ["MOUSEMOVE f f"]
    with raises(InvalidArgumentsError):
        DucklingCompiler().compile(x, skip_indentation=True)
        
    x = ["MOUSEMOVE 4 4"]
    compiled = DucklingCompiler().compile(x, skip_indentation=True)
    assert compiled.output == ["MOUSEMOVE 4 4"]