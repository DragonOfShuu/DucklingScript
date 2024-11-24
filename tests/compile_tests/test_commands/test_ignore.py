# from ducklingscript import
from ducklingscript import DucklingCompiler


def test_ignore():
    output = """
VAR x = 10
WHILE (x<20) THEN
    STRING 3.0
    STRING Code
    x = x+1
END_WHILE
"""
    code = '''
Ignore
    """
    VAR x = 10
    WHILE (x<20) THEN
        STRING 3.0
        STRING Code
        x = x+1
    END_WHILE
    """
'''
    x = DucklingCompiler().compile(code)
    assert x.output == output.strip().split("\n")
