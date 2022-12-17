from aoc_2022 import Input

ROCK, PAPER, SCISSORS = 0, 1, 2
LOSS_TIE_WIN = {ROCK: [SCISSORS, ROCK, PAPER], PAPER: [ROCK, PAPER, SCISSORS], SCISSORS: [PAPER, SCISSORS, ROCK]}


class Solution:
    def __init__(self, inp: Input):
        self.games = [(ord(line[0]) - ord("A"), ord(line[2]) - ord("X")) for line in inp.get_lines()]

    def score(self, his, mine) -> int:
        return 1 + mine + LOSS_TIE_WIN[his].index(mine) * 3

    def part_a(self):
        score_a = 0
        for his, mine in self.games:
            score_a += self.score(his, mine)
        return score_a

    def part_b(self):
        score_b = 0
        for his, strategy in self.games:
            score_b += self.score(his, LOSS_TIE_WIN[his][strategy])
        return score_b


def test_simple():
    solution = Solution(Input(0))
    assert solution.part_a() == 15
    assert solution.part_b() == 12


def test_challenge():
    solution = Solution(Input())
    assert solution.part_a() == 13052
    assert solution.part_b() == 13693
