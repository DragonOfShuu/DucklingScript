# from ducklingscript import Compiler
# from ducklingscript.cli.compiler.pre_line import PreLine
# import json as j

# parser = Compiler()

# with open("tests/compile_tests/indent_test.txt") as f:
#     x = parser._convert_to_list(PreLine.convert_to(f.read().split("\n")))

# print(j.dumps(x, indent=2))

from ducklingscript.cli.compiler.tokenization.expr_tokenizer import ExprTokenizer
from ducklingscript.cli.compiler.stack import Stack


stack = Stack([])
tokenizer = ExprTokenizer(stack)

tokenizer.set_value("2 + 2")
assert tokenizer.solve() == 4
