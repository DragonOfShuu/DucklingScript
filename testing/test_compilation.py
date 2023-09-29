from cli import Compile

def test_indent_on_compilation():
    parser = Compile()

    with open("testing/indent_test.txt") as f:
        # x = parser.parse(f.read())
        x = parser._convert_to_list(f.read().split("\n"))

    assert x==["for 5", ["REM",["Hello World","Bruv","Yes"]],"REM", ["Hello to DucklingScript"]]
