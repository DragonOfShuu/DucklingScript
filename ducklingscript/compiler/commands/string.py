from .bases import SimpleCommand, Example

desc = """
As if the user was to type text. After the command
and one space, all subsequent characters will be typed
out.

STRING simply types out the text. STRINGLN types out the
text and presses enter.
"""

duckling_ex = [
    """
STRING Hello World
""",
    '''
STRING 
    """
    This is
        some text
    """
''',
]
compiled_ex = [
    """
STRING Hello World
""",
    """
STRING this is
STRING     some text
""",
]

example_list = [
    Example(duckling=duckling_ex[0], compiled=compiled_ex[0]),
    Example(duckling=duckling_ex[1], compiled=compiled_ex[1]),
]


class String(SimpleCommand):
    names = ["STRING", "STRINGLN"]
    strip_args = False
    description = desc
