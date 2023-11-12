import pytest

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution
from solutions.python.aoc.year_2019 import IntcodeComputer
import itertools as it


class Year2019Day7(Solution):
    """2019/7: Amplification Circuit"""

    def __init__(self, inp: Input):
        self.program = list(map(int, inp.get_text().split(",")))

    def part_a(self):
        def run(phase_settings):
            inp = 0
            for phase in phase_settings:
                inp = IntcodeComputer(self.program.copy()).run([phase, inp])[0]
            return inp

        return max(map(run, it.permutations(range(5))))

    def part_b(self):
        def run(phase_settings):
            computers = []
            for phase in phase_settings:
                computers.append(IntcodeComputer(self.program.copy()))
                computers[-1].run([phase])

            inp = 0
            while inp is not None:
                for computer in computers:
                    out = computer.run([inp])
                    if not out:
                        return inp
                    inp = out[0]
            return inp

        return max(map(run, it.permutations(range(5, 10))))


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2019Day7)
