from ducklingscript.cli.compiler.tokenization.expr_tokenizer import ExprTokenizer
from ducklingscript.cli.compiler.stack import Stack


def tokenize(value: str):
    stack = Stack([])
    tokenizer = ExprTokenizer(stack)

    tokenizer.set_value(value)
    return tokenizer.solve()


def test_tokenizer_1():
    assert tokenize("2 + 2") == 4


def test_tokenizer_2():
    assert tokenize("10^2") == 100


def test_tokenizer_3():
    assert tokenize("2 + 2 * 4") == 10

def test_tokenizer_4():
    assert tokenize("(2+2) * 20") == 80