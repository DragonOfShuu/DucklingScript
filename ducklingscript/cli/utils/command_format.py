from ducklingscript import BaseCommand

import re


def format_name(command: type[BaseCommand]):
    name: str = separate_capitals(command.__name__).lower()
    name = name.removeprefix("flipper ").removeprefix("quackinter ")
    if command.flipper_only:
        name += " 🐬"

    if command.quackinter_only:
        name += " 🦆"

    return name.title()


def format_command_type(command: type[BaseCommand]):
    if command.__base__ is None:
        return "Unknown Command"
    return separate_capitals(command.__base__.__name__)


def separate_capitals(text: str):
    return re.sub(r"(\w)([A-Z])", r"\1 \2", text)
