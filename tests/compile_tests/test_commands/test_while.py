from ducklingscript import DucklingCompiler


def test_basic_while():
    x = ["WHILE count,count<3", ["STRINGLN a"]]
    answer = DucklingCompiler().compile(x, skip_indentation=True)
    assert answer.output == ["STRINGLN a", "STRINGLN a", "STRINGLN a"]


def test_advanced_while():
    x = ["REPEAT i,10", ["$STRINGLN i"]]
    answer = DucklingCompiler().compile(x, skip_indentation=True)
    assert answer.output == [
        "STRINGLN 0",
        "STRINGLN 1",
        "STRINGLN 2",
        "STRINGLN 3",
        "STRINGLN 4",
        "STRINGLN 5",
        "STRINGLN 6",
        "STRINGLN 7",
        "STRINGLN 8",
        "STRINGLN 9",
    ]
