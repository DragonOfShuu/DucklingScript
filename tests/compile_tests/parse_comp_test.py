from ducklingscript import Compile

def test_parse_comprehension():
    parser = Compile()
    with open("tests/compile_tests/parse_comp.txt") as f:
        x = parser.parse(f.read())
        assert x==["for 5", ["REM",["Hello World","Bruv","Yes"]],"REM", ["Hello to DucklingScript"]]