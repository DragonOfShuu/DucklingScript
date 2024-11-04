from ducklingscript import Compiler


def test_print_1():
    x = Compiler().compile(["PRINT Hello World"], skip_indentation=True)
    assert len(x.std_out) == 1
    assert x.std_out[0].line.content == "Hello World"
    assert x.std_out[0].file is None


def test_print_2():
    x = Compiler().compile(["PRINT 1", "PRINT 2", "PRINT 3"], skip_indentation=True)
    compiled = [i.line for i in x.std_out]

    for count, i in enumerate(compiled):
        c = count + 1
        assert i.content == str(c) and i.number == c
