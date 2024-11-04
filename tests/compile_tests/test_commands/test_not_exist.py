from ducklingscript import CompilationError, Compiler
import pytest


def test_not_exists():
    to_comp = ["NOTEXIST a"]
    x = Compiler().compile(to_comp, skip_indentation=True)
    assert x.output == []


def test_not_exists_error():
    to_comp = ['VAR a "I do exist thank you."', "NOTEXIST a"]
    with pytest.raises(CompilationError) as e:
        Compiler().compile(to_comp, skip_indentation=True)
    assert e.value.args[0] == "'a' does exist."
