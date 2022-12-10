from aoc_2022 import get_input_lines


def find_unique(text, length) -> int:
    for i in range(length, len(text)):
        if len(set(text[i - length:i])) == length:
            return i


if __name__ == "__main__":
    line = get_input_lines()[0]
    print(f"part_a: {find_unique(line, 4)}")
    print(f"part_a: {find_unique(line, 14)}")
