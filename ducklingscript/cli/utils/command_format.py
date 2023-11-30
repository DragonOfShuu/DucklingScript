from ducklingscript import BaseCommand

import re


def format_name(command: type[BaseCommand]):
    name: str = separate_capitals(command.__name__).lower()
    name = name.removeprefix("flipper ")
    if command.flipper_only:
        name += " 🐬"

    return name.title()


def separate_capitals(text: str):
    return re.sub(r"(\w)([A-Z])", r"\1 \2", text)
