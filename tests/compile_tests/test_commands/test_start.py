from ducklingscript import Compiler
from pathlib import Path

test_files = Path("tests/compile_tests/test_commands/start_test_files/")
startcode_test = test_files / "startcode_test" / "test_a.txt"
startenv_test = test_files / "startenv_test" / "test_a.txt"
start_test = test_files / "start_test" / "test_a.txt"


def test_startcode():
    compiled = Compiler().compile_file(startcode_test)
    assert compiled.output == ["STRING test b says: Hello World!"]


def test_startenv():
    compiled = Compiler().compile_file(startenv_test)
    assert compiled.output == ["STRING b: test test"]


def test_start():
    compiled = Compiler().compile_file(start_test)
    assert compiled.output == ["STRING I say hello!", "STRING He says hello!"]


def test_start_path_types():
    compiled = Compiler().compile_file(
        test_files / "start_paths" / "middle" / "test_a.txt"
    )

    assert compiled.output == ["STRING b says hello!", "STRING c says hello!"]
