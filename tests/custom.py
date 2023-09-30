from ducklingscript import Compile
import json as j

parser = Compile()

with open("tests/compile_tests/indent_test.txt") as f:
    x = parser._convert_to_list(f.read().split("\n"))

print(j.dumps(x, indent=2))