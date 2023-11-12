import pytest

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution
from textwrap import wrap


class Year2019Day8(Solution):
    """2019/8: Space Image Format"""

    def __init__(self, inp: Input):
        self.digits = inp.get_lines()[0]
        self.w = 25
        self.h = 6

    def _frame(self):
        return self.w * self.h

    def _get_layers(self):
        frame = self._frame()
        layers = []
        for layer in range(len(self.digits) // frame):
            layers.append(self.digits[layer * frame: (layer + 1) * frame])
        return layers

    def part_a(self):
        layers = self._get_layers()
        index, _ = min(enumerate(layers), key=lambda x: x[1].count('0'))
        return layers[index].count('1') * layers[index].count('2')

    def part_b(self):
        frame = self._frame()
        picture = ['2'] * frame
        for layer in self._get_layers():
            for i in range(frame):
                if picture[i] == '2':
                    picture[i] = layer[i]

        return "\n".join(wrap("".join(picture).replace("1", "#").replace("0", "."), self.w))


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2019Day8)
