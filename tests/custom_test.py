from pathlib import Path

from quackinter.config import Config
from quackinter.quackinter import interpret


CUSTOM_SCRIPT_FOLDER_NAME = "custom_test_scripts"
CUSTOM_SCRIPT_LOCATION = Path(__file__).parent / CUSTOM_SCRIPT_FOLDER_NAME


def run_test(index: int = 1):
    """
    Currently doesn't run DucklingScript,
    only DuckyScript
    """
    print("Await 1 second...")
    config = Config(
        delay=1000, output=lambda output, line: print(f"{line.line_num} -> {output}")
    )

    ducky_code = CUSTOM_SCRIPT_LOCATION / f"custom{index}.dkls"
    if not ducky_code.exists:
        print("File index given does not exist.")
        return

    return_value = interpret(ducky_code.read_text(), config)
    if return_value.error and return_value.stacktrace:
        print("Error:")
        for stack in return_value.stacktrace.traceback:
            print(f"On line {stack.line_num} -> {stack.line_content}")
        print(return_value.stacktrace.error)


def generate_tests():
    CUSTOM_SCRIPT_LOCATION.mkdir(exist_ok=True)
    custom1 = CUSTOM_SCRIPT_LOCATION / "custom1.dkls"
    custom1.write_text(
        """WIN
DELAY 1000
STRINGLN edge
DELAY 1000
STRINGLN https://www.youtube.com/watch?v=dQw4w9WgXcQ&autoplay=true
DELAY 5000
WAITFORBUTTONPRESS GOTTEM
REPEAT 2
"""
    )
    print('Generation complete! Run "poetry run poe test" to run!')
