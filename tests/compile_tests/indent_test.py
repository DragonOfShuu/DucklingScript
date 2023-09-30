from ducklingscript import Compile, CompilationError
import pytest

def test_indent_on_compilation_end():
    parser = Compile()

    with pytest.raises(CompilationError) as exc_info:
        with open("tests/compile_tests/indent_test.txt") as f:
            x = parser._convert_to_list(f.read().split("\n"))
            print(x)

    assert exc_info.value.args[0] == "Tab is not equivalent to the others on line 12"

def test_indent_on_compilation_mid():
    parser = Compile()

    with pytest.raises(CompilationError) as exc_info:
        with open("tests/compile_tests/indent_test_2.txt") as f:
            x = parser._convert_to_list(f.read().split("\n"))
            print(x)

    assert exc_info.value.args[0] == "Tab is not equivalent to the others on line 3"