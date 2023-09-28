from cli.compile import Compile,ParserOptions

parser = Compile()

with open("testing/test_script.txt") as f:
    x = parser.parse(f.read())

print(x)