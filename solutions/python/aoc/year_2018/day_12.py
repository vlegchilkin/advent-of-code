import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution


class Year2018Day12(Solution):
    """2018/12: Subterranean Sustainability"""

    def __init__(self, inp: Input):
        it = inp.get_iter()
        self.init_state = next(it).split("initial state: ")[-1]
        next(it)
        self.lines = [line.split(" => ") for line in it]

    def run(self, n):
        ref = {r[0]: r[1] for r in self.lines}
        state = self.init_state
        res, delta = None, []
        for t in range(n):
            buffer, state = f"....{state}....", ""
            for i in range(2, len(buffer) - 2):
                state += ref.get(buffer[i - 2 : i + 3]) or "."

            _res = res or 0
            res = sum((i - (t + 1) * 2) for i, c in enumerate(state) if c == "#")
            delta.append(res - _res)
            if t > 5 and delta[-5:].count(delta[-1]) == 5:
                res += (n - t - 1) * delta[-1]
                break
        return res

    def part_a(self):
        return self.run(20)

    def part_b(self):
        return self.run(50_000_000_000)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2018Day12)
