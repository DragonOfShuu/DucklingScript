from ducklingscript.cli.compiler.tokenization.expr_tokenizer import ExprTokenizer
from ducklingscript.cli.compiler.stack import Stack


def test_tokenizer_1():
    stack = Stack([])
    tokenizer = ExprTokenizer(stack)

    tokenizer.set_value("2 + 2")
    assert tokenizer.solve() == 4
