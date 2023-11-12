import pytest

from solutions.python.aoc import Input, get_puzzles, PuzzleData, parse_with_template, Solution
from solutions.python.aoc.space import to_str


class Year2021Day13(Solution):
    def __init__(self, inp: Input):
        it = inp.get_iter()
        self.dots = set()
        while line := next(it):
            self.dots.add(complex(*map(int, line.split(","))))

        self.folds = [parse_with_template(line, "fold along {{axis}}={{x|to_int}}")[0] for line in it]

    @staticmethod
    def fold(dots, fold):
        fold_func = {
            "x": lambda d, x=fold.x: d if (diff := d.real - x) < 0 else d - 2 * diff,
            "y": lambda d, x=fold.x: d if (diff := d.imag - x) < 0 else d - 2j * diff,
        }[fold.axis]

        return set(map(fold_func, dots))

    def part_a(self):
        return len(self.fold(self.dots, self.folds[0]))

    def part_b(self):
        dots = self.dots
        for fold in self.folds:
            dots = self.fold(dots, fold)
        return to_str(dots, True).replace("1", "#").replace("0", ".")


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2021Day13)
