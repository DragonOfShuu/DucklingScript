from pathlib import Path

from ducklingscript import DucklingCompiler

test_files = Path("tests/compile_tests/test_commands/from_test_files/")

def test_variable_import():
    path = test_files / "variable_import" / "main.dkls"
    compiled = DucklingCompiler().compile_file(path)
    assert compiled.output[0] == "STRINGLN I like trains."
    assert compiled.output[1] == "STRINGLN DEAD"

def test_function_import():
    path = test_files / "function_import" / "main.dkls"
    compiled = DucklingCompiler().compile_file(path)
    assert compiled.output[0] == "STRINGLN Hello world!"

def test_function_env_persistence():
    path = test_files / "function_env_persistence" / "main.dkls"
    compiled = DucklingCompiler().compile_file(path)
    assert compiled.output[0] == "STRINGLN 0"
    assert compiled.output[1] == "STRINGLN 1"
    assert compiled.output[2] == "STRINGLN 2"
    assert compiled.output[3] == "STRINGLN 3"
    assert compiled.output[4] == "STRINGLN 4"