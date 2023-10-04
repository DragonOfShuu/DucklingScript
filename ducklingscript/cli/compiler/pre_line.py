from __future__ import annotations


class PreLine:
    def __init__(self, content: str, line_num: int) -> None:
        self.content = content
        self.number = line_num

    @staticmethod
    def convert_to(lines: list[str]) -> list[PreLine]:
        return [PreLine(line, line_num + 1) for line_num, line in enumerate(lines)]

    @staticmethod
    def convert_from(lines: list[PreLine | list] | list[PreLine]) -> list[str]:
        returnable = []
        for i in lines:
            if isinstance(i, list):
                returnable.append(PreLine.convert_from(i))
            else:
                returnable.append(i.content)
        return returnable

        # return [i.content for i in lines]
