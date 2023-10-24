from ducklingscript import Compiler


def test_basic_repeat():
    x = ["REPEAT 3", ["STRINGLN a"]]
    answer = Compiler().compile(x, skip_indentation=True)
    assert answer.output == ["STRINGLN a", "STRINGLN a", "STRINGLN a"]


def test_advanced_repeat():
    x = ["REPEAT i,10", ["$STRINGLN i"]]
    answer = Compiler().compile(x, skip_indentation=True)
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
