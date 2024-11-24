from typing import Any
from ducklingscript import DucklingCompiler
from ducklingscript.compiler.pre_line import PreLine


def __convert_to_string(the_list: list[PreLine | list]) -> Any:
    returnable_list: list[str] | list = []
    for i in the_list:
        if isinstance(i, list):
            returnable_list.append(__convert_to_string(i))
        else:
            returnable_list.append(i.content)
    return returnable_list


def test_parse_comprehension():
    parser = DucklingCompiler()
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
