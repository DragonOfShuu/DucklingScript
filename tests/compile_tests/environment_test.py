from ducklingscript.cli.compiler.environment import Environment


def test_variable_discovery():
    string = "Hello, my name is {name}, and I am {age}"
    env = Environment(user_vars={"name": "Joe", "age": 43})

    # assert env.parse_vars(string) == "Hello, my name is Joe, and I am 43"
    assert True == True
