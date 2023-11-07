from ducklingscript import Compiler
from pathlib import Path

test_files = Path('tests/compile_tests/test_commands/func_test_files/')

def test_func_1():
    test1 = test_files / "test_func_1.txt"
    x = Compiler().compile_file(test1)
    assert len(x.output)==1
    assert x.output[0]=="STRING Hello World!"

def test_func_2():
    test1 = test_files / "test_func_2.txt"
    x = Compiler().compile_file(test1)
    out = []
    for i in range(5):
        out.append(f"[{i}] Hello World!")
    assert len(x.output)==0
    assert [i.line.content for i in x.std_out] == out