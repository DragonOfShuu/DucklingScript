from ducklingscript import Environment, EnvExtendType


def test_variable_environment_1():
    env = Environment().var
    env.new_user_var("x", 10)
    assert env.get_user_var("x").value == 10


def test_variable_environment_2():
    env = Environment().var
    env.new_user_var("y", 20)
    assert env.get_user_var("y").value == 20
    env.new_user_var("y", 30)
    assert env.get_user_var("y").value == 30


def test_variable_environment_3():
    env = Environment()
    env.var.new_user_var("z", 40)
    assert env.var.get_user_var("z").value == 40
    extend_env = env.extend_env(None, None, extend_type=EnvExtendType.PARALLEL)
    extend_env.var.new_user_var("z", 50)
    assert extend_env.var.get_user_var("z").value == 50
    assert env.var.get_user_var("z").value == 50  # Original environment should change
