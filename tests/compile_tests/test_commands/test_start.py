from ducklingscript import DucklingCompiler
from pathlib import Path

test_files = Path("tests/compile_tests/test_commands/start_test_files/")
startcode_test = test_files / "startcode_test" / "test_a.dkls"
startenv_test = test_files / "startenv_test" / "test_a.dkls"
start_test = test_files / "start_test" / "test_a.dkls"


def test_startcode():
    compiled = DucklingCompiler().compile_file(startcode_test)
    assert compiled.output == ["STRING test b says: Hello World!"]


def test_startenv():
    compiled = DucklingCompiler().compile_file(startenv_test)
    assert compiled.output == ["STRING b: test test"]


def test_start():
    compiled = DucklingCompiler().compile_file(start_test)
    assert compiled.output == ["STRING I say hello!", "STRING He says hello!"]


def test_start_path_types():
    compiled = DucklingCompiler().compile_file(
        test_files / "start_paths" / "middle" / "test_a.dkls"
    )

    assert compiled.output == ["STRING b says hello!", "STRING c says hello!"]
