from ducklingscript import Compiler

def test_print_1():
    x = Compiler().compile(["PRINT Hello World"], skip_indentation=True)
    assert len(x.std_out)==1
    assert x.std_out[0].line.content == "Hello World"
    assert x.std_out[0].file == None