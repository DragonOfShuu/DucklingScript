class CompilationError(Exception):
    pass

class StackOverflowError(CompilationError): pass

# class IndentationError(CompilationError):
#     pass