import pytest
from ducklingscript.compiler.environments.environment import Environment
from ducklingscript.compiler.tokenization import Tokenizer
from ducklingscript.compiler.environments.variable_environment import (
    VariableEnvironment,
)
from ducklingscript import DivideByZeroError, ExpectedTokenError, MismatchError


tokenize = Tokenizer.tokenize


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
    assert tokenize("2/2") == 1


def test_tokenizer_9():
    assert not tokenize("5 < 2==1")


def test_tokenizer_10():
    assert tokenize('"Hello"!="hello"')


def test_tokenizer_11():
    assert tokenize('"Hello World"') == "Hello World"


def test_tokenizer_12():
    with pytest.raises(DivideByZeroError):
        tokenize("20 / 0")


def test_tokenizer_13():
    with pytest.raises(ExpectedTokenError) as e:
        tokenize("20=20")
    assert e.value.args[0] == "A valid operand was expected"


def test_tokenizer_14():
    with pytest.raises(ExpectedTokenError) as e:
        tokenize("e==1")
    assert "A valid value was expected" == e.value.args[0]


def test_tokenizer_15():
    with pytest.raises(MismatchError) as e:
        tokenize('"Hello World~"*2')
    assert (
        e.value.args[0] == "Operand * is not supported for type 'Hello World~' and '2'"
    )


def test_tokenizer_16():
    assert tokenize("5.") == 5.0


def test_tokenizer_17():
    with pytest.raises(ExpectedTokenError) as e:
        tokenize("5..")
    assert e.value.args[0] == "A valid operand was expected"


def test_tokenizer_18():
    with pytest.raises(ExpectedTokenError) as e:
        tokenize("(5+5))==10")
    assert e.value.args[0] == "A valid operand was expected"


def test_tokenizer_19():
    with pytest.raises(ExpectedTokenError) as e:
        tokenize("((5+4)==9")
    assert e.value.args[0] == "Expected a closing parenthesis"


def test_tokenizer_20():
    assert tokenize("TRUE") is True


def test_tokenizer_21():
    assert tokenize("FALSE") is False


def test_tokenizer_22():
    assert tokenize("TRUE!=FALSE==TRUE")


def test_tokenizer_23():
    assert tokenize("(TRUE==FALSE)==FALSE")


def test_tokenizer_24():
    with pytest.raises(ExpectedTokenError):
        assert tokenize("(TRUE==)==0")


def test_tokenizer_25():
    assert tokenize("FALSE==0") is True


def test_tokenizer_26():
    assert tokenize('FALSE == "FALSE" == FALSE')


def test_tokenizer_27():
    env = Environment(VariableEnvironment(user_vars={"hello": 2}))
    assert tokenize("hello==2", env=env)


def test_tokenizer_28():
    with pytest.raises(ExpectedTokenError) as e:
        env = Environment(VariableEnvironment(user_vars={"hello": 2}))
        tokenize("hell==2", env=env)
    assert e.value.args[0] == "A valid value was expected"


def test_tokenizer_29():
    with pytest.raises(ExpectedTokenError) as e:
        env = Environment(VariableEnvironment(user_vars={"hell": 2}))
        tokenize("hell2", env=env)
    assert e.value.args[0] == "A valid operand was expected"


def test_tokenizer_30():
    assert tokenize('(")))"==")))")')


def test_tokenizer_31():
    assert tokenize("(5==5)")


def test_tokenizer_32():
    assert tokenize("(5+(5+(5+10)+2))") == 27


def test_tokenizer_33():
    assert tokenize("!(FALSE)")


def test_tokenizer_34():
    assert tokenize("!(0)")


def test_tokenizer_35():
    assert tokenize("!(1)==FALSE")


def test_tokenizer_36():
    assert not tokenize('!("Hello World")')


def test_tokenizer_37():
    assert tokenize("20 / 10 == 2")


def test_tokenizer_38():
    assert tokenize("-20") == -20


def test_tokenizer_39():
    assert tokenize("30--30") == 60


def test_tokenizer_40():
    with pytest.raises(ExpectedTokenError):
        tokenize("-")


def test_tokenizer_41():
    with pytest.raises(ExpectedTokenError):
        tokenize("-+")


def test_tokenizer_42():
    with pytest.raises(ExpectedTokenError):
        tokenize(".")


def test_tokenizer_43():
    assert tokenize("(5+5) * (5+5) * ((1+1)*(1+1))") == 400
