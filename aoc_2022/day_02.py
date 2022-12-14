from aoc_2022 import Input

ROCK, PAPER, SCISSORS = 0, 1, 2
loss_tie_win = {ROCK: [SCISSORS, ROCK, PAPER], PAPER: [ROCK, PAPER, SCISSORS], SCISSORS: [PAPER, SCISSORS, ROCK]}


def part_a(his, mine) -> int:
    return 1 + mine + loss_tie_win[his].index(mine) * 3


def part_b(his, st) -> int:
    return part_a(his, loss_tie_win[his][st])


if __name__ == "__main__":
    score_a = score_b = 0
    for line in Input().get_lines():
        first, second = ord(line[0]) - ord("A"), ord(line[2]) - ord("X")
        score_a += part_a(first, second)
        score_b += part_b(first, second)

    print(f"part_a: {score_a}")
    print(f"part_b: {score_b}")
