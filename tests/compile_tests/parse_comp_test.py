from typing import Any
from ducklingscript import Compiler
from ducklingscript.compiler.pre_line import PreLine


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
        assert x.output == [
            "STRING Hello World",
            "STRING Bruv",
            "STRING Yes",
            "STRING Hello World",
            "STRING Bruv",
            "STRING Yes",
            "STRING Hello World",
            "STRING Bruv",
            "STRING Yes",
            "STRING Hello World",
            "STRING Bruv",
            "STRING Yes",
            "STRING Hello World",
            "STRING Bruv",
            "STRING Yes",
            "STRING Hello to DucklingScript",
        ]
