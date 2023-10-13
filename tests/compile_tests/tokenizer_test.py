from ducklingscript.cli.compiler.tokenization.expr_tokenizer import ExprTokenizer
from ducklingscript.cli.compiler.stack import Stack


def tokenize(value: str):
    stack = Stack([])
    tokenizer = ExprTokenizer(stack, value)

    # tokenizer.set_value(value)
    return tokenizer.solve()


def test_tokenizer_1():
    assert tokenize("2 + 2") == 4


def test_tokenizer_2():
    assert tokenize("10^2") == 100


def test_tokenizer_3():
    assert tokenize("2 + 2 * 4") == 10


def test_tokenizer_4():
    assert tokenize("2==2")


def test_tokenizer_5():
    assert tokenize("(2+2) * 20") == 80


def test_tokenizer_6():
    assert tokenize("(20*2^2)==80")


def test_tokenizer_7():
    assert tokenize("2*2*2+5!=14")


def test_tokenizer_8():
    assert not tokenize("5 < 2")
    