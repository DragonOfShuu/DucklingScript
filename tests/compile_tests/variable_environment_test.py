from ducklingscript import VariableEnvironment, Environment, EnvExtendType


def test_variable_environment_1():
    env = VariableEnvironment()
    env.new_user_var("x", 10)
    assert env.get_user_var("x") == 10


def test_variable_environment_2():
    env = VariableEnvironment()
    env.new_user_var("y", 20)
    assert env.get_user_var("y") == 20
    env.new_user_var("y", 30)
    assert env.get_user_var("y") == 30


def test_variable_environment_3():
    # env = VariableEnvironment()
    # env.extend_env(None)
    env = Environment()
    env.var.new_user_var("z", 40)
    assert env.var.get_user_var("z") == 40
    extend_env = env.extend_env(None, None, extend_type=EnvExtendType.PARALLEL)
    extend_env.var.new_user_var("z", 50)
    assert extend_env.var.get_user_var("z") == 50
    assert env.var.get_user_var("z") == 50  # Original environment should change
