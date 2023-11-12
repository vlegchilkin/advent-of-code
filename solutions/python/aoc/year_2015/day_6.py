import re
from enum import StrEnum
from typing import Callable

import numpy as np
import pytest

from solutions.python.aoc import Input, get_puzzles, PuzzleData, Solution


class Action(StrEnum):
    TURN_ON = "turn on"
    TURN_OFF = "turn off"
    TOGGLE = "toggle"


ACTION = re.compile(rf"^({Action.TURN_ON}|{Action.TURN_OFF}|{Action.TOGGLE}) (\d+),(\d+) through (\d+),(\d+)$")


class Year2015Day6(Solution):
    def __init__(self, inp: Input):
        data = [re.match(ACTION, line).groups() for line in inp.get_lines()]
        self.actions = [(Action(d[0]), int(d[1]), int(d[2]), int(d[3]), int(d[4])) for d in data]

    def make_actions(self, func: Callable[[Action, np.ndarray], np.ndarray]):
        a = np.zeros((1000, 1000), dtype=int)
        for action, r_min, c_min, r_max, c_max in self.actions:
            a[r_min : r_max + 1, c_min : c_max + 1] = func(action, a[r_min : r_max + 1, c_min : c_max + 1])
        return np.sum(a)

    def part_a(self):
        def func(action: Action, a: np.ndarray):
            match action:
                case Action.TURN_ON:
                    return 1
                case Action.TURN_OFF:
                    return 0
                case Action.TOGGLE:
                    return 1 - a

        return self.make_actions(func)

    def part_b(self):
        def func(action: Action, a: np.ndarray):
            match action:
                case Action.TURN_ON:
                    return a + 1
                case Action.TURN_OFF:
                    a[a == 0] = 1
                    return a - 1
                case Action.TOGGLE:
                    return a + 2

        return self.make_actions(func)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2015Day6)
