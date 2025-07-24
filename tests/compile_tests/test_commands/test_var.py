
from ducklingscript import DucklingCompiler


def test_var_1():
    """
    Test the variable command.
    """
    code = """
VAR x 5
LOCALVAR y 10
"""
    compiled = DucklingCompiler().compile(code)
    assert compiled.env.var.get_user_var("x").value == 5
    assert compiled.env.var.get_user_var("y").value == 10

def test_var_2():
    """
    Test the variable command with an existing variable.
    """
    code = """
VAR x 5
LOCALVAR y 10
VAR x 15
LOCALVAR y 20
"""
    compiled = DucklingCompiler().compile(code)
    assert compiled.env.var.get_user_var("x").value == 15
    assert compiled.env.var.get_user_var("y").value == 20

def test_localvar():
    """
    Test the local variable command.
    """
    code = """
VAR x 5
VAR y 5

FUNCTION test_func
    LOCALVAR x 10
    VAR y 10
    $STRINGLN x + y

RUN test_func

REM X should be 5
REM y should be 15
"""
    compiled = DucklingCompiler().compile(code)
    assert compiled.env.var.get_user_var("x").value == 5
    assert compiled.env.var.get_user_var("y").value == 10
    assert compiled.output[0] == "STRINGLN 20"
