import pytest

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution


class Year2018Day8(Solution):
    """2018/8: Memory Maneuver"""

    def __init__(self, inp: Input):
        self.data = inp.get_lines(lambda line: list(map(int, line.split(" "))))[0]

    def part_a(self):
        def recu(it):
            nodes, md = next(it), next(it)
            return sum(recu(it) for _ in range(nodes)) + sum(next(it) for _ in range(md))

        return recu(iter(self.data))

    def part_b(self):
        def recu(it):
            nodes, md = next(it), next(it)
            _nodes = [recu(it) for _ in range(nodes)]
            _md = [next(it) for _ in range(md)]

            if nodes == 0:
                return sum(_md)

            return sum(_nodes[i - 1] for i in _md if i <= nodes)

        return recu(iter(self.data))


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2018Day8)
