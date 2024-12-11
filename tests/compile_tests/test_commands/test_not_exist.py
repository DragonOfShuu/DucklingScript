from ducklingscript import DucklingScriptError, DucklingCompiler
import pytest


def test_not_exists():
    to_comp = ["NOTEXIST a"]
    x = DucklingCompiler().compile(to_comp, skip_indentation=True)
    assert x.output == []


def test_not_exists_error():
    to_comp = ['VAR a "I do exist thank you."', "NOTEXIST a"]
    with pytest.raises(DucklingScriptError) as e:
        DucklingCompiler().compile(to_comp, skip_indentation=True)
    assert e.value.args[0] == "'a' does exist."
