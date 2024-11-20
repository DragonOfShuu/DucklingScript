from __future__ import annotations


class PreLine:
    """
    Stores a line of code.

    Args:
        content: The content of the line being stored (usually without a whitespace)
        line_num: The line number the line is on. This value is one-based.
        file_index: The file index of the line being stored. This value is zero-based.
    """

    def __init__(self, content: str, line_num: int, file_index: int) -> None:
        self.content = content
        self.number = line_num
        self.file_index = file_index

    @staticmethod
    def convert_to(lines: list[str], file_index: int) -> list[PreLine]:
        """
        Recursively convert from
        a list of strings to a
        list of PreLines.
        """
        return [
            PreLine(line, line_num + 1, file_index)
            for line_num, line in enumerate(lines)
        ]

    @staticmethod
    def convert_to_recur(lines: list, file_index: int, line_num_offset: int = 0):
        returnable = []
        line_num = line_num_offset
        for i in lines:
            line_num += 1
            if isinstance(i, list):
                returnable.append(PreLine.convert_to_recur(i, file_index, line_num - 1))
                line_num += len(i) - 1
                continue
            else:
                returnable.append(PreLine(i, line_num, file_index))
        return returnable

    @staticmethod
    def convert_from(lines: list[PreLine | list] | list[PreLine]) -> list[str]:
        """
        Recursively convert from
        a list of PreLines to a
        list of strings.
        """
        returnable = []
        for i in lines:
            if isinstance(i, list):
                returnable.append(PreLine.convert_from(i))
            else:
                returnable.append(i.content)
        return returnable

    def cont_upper(self):
        return self.content.upper()

    def __repr__(self) -> str:
        return self.content

    def __eq__(self, value: object) -> bool:
        if isinstance(value, int):
            return value == self.number
        elif isinstance(value, str):
            return value == self.content
        elif isinstance(value, PreLine):
            # print("checking same")
            # print(f"Value Content: {value.content}")
            # print(f"Self Content: {self.content}")
            # print(f"Value Number: {value.number}")
            # print(f"Self Number: {self.number}")
            # print(f"Value File: {value.file_index}")
            # print(f"Self File: {self.file_index}")
            return value.number == self.number and value.file_index == self.file_index
        else:
            return False
