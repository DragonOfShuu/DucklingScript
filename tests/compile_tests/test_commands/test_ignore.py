# from ducklingscript import
from ducklingscript import Compiler
import pytest


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
    x = Compiler().compile(code)
    assert x.output == output.strip().split("\n")
