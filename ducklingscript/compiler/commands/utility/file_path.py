from typing import Any, TYPE_CHECKING
from pathlib import Path

from ...errors import (
    CircularStructureError,
    InvalidArgumentsError,
    UnexpectedTokenError,
)

if TYPE_CHECKING:
    from ...stack_pile import StackPile

script_extension = ".dkls"


def convert_to_path(
    stack_pile: "StackPile", current_file: Path, relative_path: str
) -> Path:
    """
    Convert a dot separated, relative file path into 
    the file being referenced. 
    """

    # Folder the stack is inside
    if current_file is None:
        raise TypeError("Stack should not be None here. This should be impossible")
    stack_wf: Path = current_file.parent

    relative_path, stack_wf = go_up_directories(relative_path, stack_wf, stack_pile)

    if ".." in relative_path:
        raise UnexpectedTokenError(
            stack_pile,
            "The dot operator can only be used once in between each folder/file name.",
        )

    path = Path(relative_path.replace(".", "/") + script_extension)
    new_file = stack_wf.joinpath(path)
    if not new_file.exists() or not new_file.is_file():
        raise InvalidArgumentsError(
            stack_pile, "The path must point to a file, and it must exist."
        )

    check_for_circles(new_file, stack_pile)

    return new_file


def go_up_directories(
    relative_path: str, stack_wf: Path, stack_pile: "StackPile"
) -> tuple[str, Path]:
    while relative_path.startswith("."):
        if stack_wf.parent == stack_wf:
            raise UnexpectedTokenError(
                stack_pile,
                "Too many dots before the path name. Already at the drive root.",
            )
        stack_wf = stack_wf.parent
        relative_path = relative_path[1:]
    return relative_path, stack_wf


def check_for_circles(similar_import: Path, stack_pile: "StackPile"):
    for i in stack_pile:
        i: Any
        if i.file == similar_import:
            raise CircularStructureError(
                stack_pile,
                "A circular structure is being created by a file importing another file that is importing the original file.",
            )
