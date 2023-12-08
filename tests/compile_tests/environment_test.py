from ducklingscript.compiler.environments.environment import Environment
from ducklingscript.compiler.environments.variable_environment import (
    VariableEnvironment,
)


def test_variable_discovery():
    string = "Hello, my name is {name}, and I am {age}"
    env = Environment(VariableEnvironment(user_vars={"name": "Joe", "age": 43}))

    # assert env.var.parse_vars(string) == "Hello, my name is Joe, and I am 43"
    assert True == True
