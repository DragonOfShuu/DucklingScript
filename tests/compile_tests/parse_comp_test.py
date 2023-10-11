from typing import Any
from ducklingscript import Compiler
from ducklingscript.cli.compiler.pre_line import PreLine


def __convertToString(the_list: list[PreLine | list]) -> Any:
    returnable_list: list[str] | list = []
    for i in the_list:
        if isinstance(i, list):
            returnable_list.append(__convertToString(i))
        else:
            returnable_list.append(i.content)
    return returnable_list


def test_parse_comprehension():
    parser = Compiler()
    with open("tests/compile_tests/parse_comp.txt") as f:
        x = parser.compile(f.read())
        # assert x[0] == [
        #     "for 5",
        #     ["REM", ["Hello World", "Bruv", "Yes"]],
        #     "REM",
        #     ["Hello to DucklingScript"],
        # ]
        assert x[0] == [
            "REM Hello World",
            "REM Bruv",
            "REM Yes",
            "REM Hello World",
            "REM Bruv",
            "REM Yes",
            "REM Hello World",
            "REM Bruv",
            "REM Yes",
            "REM Hello World",
            "REM Bruv",
            "REM Yes",
            "REM Hello World",
            "REM Bruv",
            "REM Yes",
            "REM Hello to DucklingScript"
        ]
