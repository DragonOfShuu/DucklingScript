from pathlib import Path
from ducklingscript import DucklingCompiler

test_files = Path("tests/compile_tests/test_commands/import_export_test_files/")


def test_import_variables():
    path = test_files / "import_variables" / "main.dkls"
    compiled = DucklingCompiler().compile_file(path)
    assert compiled.output[0] == "STRINGLN a is: 11"


def test_import_functions():
    path = test_files / "import_functions" / "main.dkls"
    compiled = DucklingCompiler().compile_file(path)
    assert compiled.output[0] == "STRINGLN Count is now: 1"
    assert compiled.output[1] == "STRINGLN Count is now: 2"
    assert compiled.output[2] == "STRINGLN Count is now: 3"
    assert compiled.output[3] == "STRINGLN Count is now: 4"
    assert compiled.output[4] == "STRINGLN Count is now: 5"

def test_import_variables_non_containerized():
    path = test_files / "import_variables_non_containerized" / "main.dkls"
    compiled = DucklingCompiler().compile_file(path)
    assert compiled.output[0] == "STRINGLN Hello world!"
