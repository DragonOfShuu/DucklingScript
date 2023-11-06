from ducklingscript import Compiler


def test_if_1():
    code = ["VAR a 2", "IF a==2", ["VAR a 3"]]
    compiled = Compiler().compile(code, skip_indentation=True)
    assert compiled.env.user_vars.get("a") == 3


def test_if_2():
    code = [
        "VAR a 1",
        "IF a>1",
        ["RETURN"],
        "ELIF a<1",
        ["RETURN"],
        "ELSE",
        ["VAR a 0"],
    ]
    compiled = Compiler().compile(code, skip_indentation=True)
    for i in compiled.std_out:
        print(i.line.content)
    print([i.error for i in compiled.warnings])
    assert compiled.env.user_vars.get("a") == 0


def test_if_3():
    code = """
VAR a 2
VAR b 1
VAR success FALSE
IF a>b
    IF a>b
        VAR success TRUE
ELIF a>b
    VAR success FALSE
$PRINT success
    """
    print(code)
    compiled = Compiler().compile(code)
    print(compiled.env.user_vars)
    print([i.line.content for i in compiled.std_out])
    assert compiled.env.user_vars.get("success")
