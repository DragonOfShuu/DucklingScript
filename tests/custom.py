from ducklingscript import Compiler
from ducklingscript.cli.compiler.pre_line import PreLine
import json as j

parser = Compiler()

with open("tests/compile_tests/indent_test.txt") as f:
    x = parser._convert_to_list(PreLine.convert_to(f.read().split("\n")))

print(j.dumps(x, indent=2))
