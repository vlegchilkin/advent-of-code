import string

import pytest

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution


class Year2017Day16(Solution):
    """2017/16: Permutation Promenade"""

    def __init__(self, inp: Input):
        self.commands = inp.get_lines(lambda line: line.split(","))[0]
        self.n = 16

    def part_a_b(self):
        buffer = list(string.ascii_lowercase[: self.n])
        visited = ["".join(buffer)]

        def step() -> str:
            nonlocal buffer
            for cmd in self.commands:
                match cmd[0]:
                    case "s":
                        k = int(cmd[1:])
                        buffer = buffer[-k:] + buffer[: self.n - k]
                    case "x":
                        a, b = map(int, cmd[1:].split("/"))
                        buffer[a], buffer[b] = buffer[b], buffer[a]
                    case "p":
                        a, b = map(buffer.index, cmd[1:].split("/"))
                        buffer[a], buffer[b] = buffer[b], buffer[a]
            return "".join(buffer)

        while (v := step()) != visited[0]:
            visited.append(v)

        return visited[1], visited[1_000_000_000 % len(visited)]


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2017Day16)
