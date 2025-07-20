from ducklingscript import StackPile, DucklingCompiler, Environment


def test_stack_pile():
    stack_pile = StackPile(
        DucklingCompiler._prepare_for_stack(["STRINGLN Hello World"]), None, None
    )
    ducky = stack_pile.start()
    assert ducky.data[0].ducky_line == "STRINGLN Hello World"


def test_stack_pile_variable_set():
    code = ["VAR a 2", "$STRINGLN a"]
    env = Environment()
    stack_pile = StackPile(DucklingCompiler._prepare_for_stack(code), None, env)
    ducky = stack_pile.start()
    assert ducky.get_ducky() == ["STRINGLN 2"]
    assert env.var.get_user_var("a").value == 2
