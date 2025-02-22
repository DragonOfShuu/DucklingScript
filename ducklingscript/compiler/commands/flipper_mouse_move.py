from ducklingscript.compiler.commands.bases.simple_command import ArgLine
from .bases.doc_command import ArgReqType
from .bases.simple_command import SimpleCommand

desc = """
Move mouse in certain direction and amount
"""

class FlipperMouseMove(SimpleCommand):
    names = ["MOUSEMOVE", "MOUSE_MOVE"]
    description = desc
    flipper_only = True
    arg_req = ArgReqType.REQUIRED

    def verify_arg(self, arg: ArgLine) -> str | None:
        arg_parts: list[str] = arg.content.split(' ')
        if len(arg_parts) != 2:
            return "Exactly two arguments are required"
        
        if not all([i.isdigit() for i in arg_parts]):
            return 'Both arguments must be an integer.'
        