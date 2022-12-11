from aoc_2022 import Input


def find_unique(text, length) -> int:
    for i in range(length, len(text)):
        if len(set(text[i - length:i])) == length:
            return i


if __name__ == "__main__":
    line = Input().get_lines()[0]
    print(f"part_a: {find_unique(line, 4)}")
    print(f"part_a: {find_unique(line, 14)}")
