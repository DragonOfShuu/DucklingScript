
from .bases.doc_command import ArgReqType
from ducklingscript.compiler.commands.bases.simple_command import ArgLine
from .bases.simple_command import SimpleCommand

import re 

desc = """
Set the device ID of the flipper
"""

class FlipperDeviceId(SimpleCommand):
    names = ["ID"]
    flipper_only = True
    description = desc
    arg_req = ArgReqType.REQUIRED

    def verify_arg(self, arg: ArgLine) -> str | None:
        content: str = arg.content
        arg_parts: list[str] = content.split(' ', 1)
        
        first_matchable = re.match(r"^[\w\d]+:[\w\d]+$", arg_parts[0])
        if first_matchable is None:
            return "For the first argument, you must do: VID:PID"

        if len(arg_parts) == 1:
            return None

        second_matchable = re.match(r"^[\w\d\s]+:[\w\d\s]+$", arg_parts[1])
        if second_matchable is None:
            return "The second argument is OPTIONAL, but must be: Manufacturer:Product"