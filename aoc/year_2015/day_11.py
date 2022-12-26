import pytest

from aoc import Input, get_puzzles, PuzzleData


class Solution:
    def __init__(self, inp: Input):
        self.password = inp.get_lines()[0]

    @staticmethod
    def _meet_requirements(password) -> bool:
        if any((c in password) for c in "iol"):
            return False

        for i in range(len(password) - 2):
            if ord(password[i]) == ord(password[i + 1]) - 1 == ord(password[i + 2]) - 2:
                break
        else:
            return False

        for first_double in range(len(password) - 3):
            if password[first_double] == password[first_double + 1]:
                break
        else:
            return False

        for second_double in range(first_double + 2, len(password) - 1):
            if password[second_double] == password[second_double + 1]:
                break
        else:
            return False

        return True

    @staticmethod
    def _increase(password, pos) -> str:
        if pos < 0:
            return "a" + password

        next_digit = chr(ord(password[pos]) + 1)
        if next_digit <= "z":
            return password[:pos] + next_digit + password[pos + 1 :]

        password = password[:pos] + "a" + password[pos + 1 :]
        return Solution._increase(password, pos - 1)

    def _next_password(self, password) -> str:
        while password := self._increase(password, len(password) - 1):
            if self._meet_requirements(password):
                return password

    def part_a(self):
        return self._next_password(self.password)

    def part_b(self):
        return self._next_password(self.part_a())


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Solution)
