from ducklingscript import Compiler, CompilationError, InvalidTabError
from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.tab_parse import parse_document
import pytest


def test_indent_on_compilation_end():
    parser = Compiler()

    with pytest.raises(CompilationError) as exc_info:
        with open("tests/compile_tests/indent_test.txt") as f:
            x = parse_document(PreLine.convert_to(f.read().split("\n")))
            print(x)

    assert exc_info.value.args[0] == "Tab is not equivalent to the others on line 13"


def test_indent_on_compilation_mid():
    parser = Compiler()

    with pytest.raises(CompilationError) as exc_info:
        with open("tests/compile_tests/indent_test_2.txt") as f:
            x = parse_document(PreLine.convert_to(f.read().split("\n")))
            print(x)

    assert exc_info.value.args[0] == "Tab is not equivalent to the others on line 3"


def test_unexpected_indent():
    parser = Compiler()

    with pytest.raises(InvalidTabError) as exc_info:
        with open("tests/compile_tests/indent_unexpected.txt") as f:
            x = parse_document(PreLine.convert_to(f.read().split("\n")))
            print(x)
    assert exc_info.value.args[0] == "Unexpected tab on line 7"
