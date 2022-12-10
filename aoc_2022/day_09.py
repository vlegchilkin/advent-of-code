from aoc_2022 import get_input_lines

DIRECTIONS = {"U": (-1, 0), "D": (1, 0), "R": (0, 1), "L": (0, -1)}


def calc_move(head, tail):
    diff = head[0] - tail[0], head[1] - tail[1]
    abs_diff = abs(diff[0]) + abs(diff[1])

    if diff[0] * diff[1] == 0 and abs_diff > 1:  # straight
        return (diff[0] // 2), (diff[1] // 2)
    elif abs_diff > 2:  # diagonal
        return -1 if diff[0] < 0 else 1, -1 if diff[1] < 0 else 1


def count(moves, chains):
    visited = set()
    rope = [(0, 0) for _ in range(chains)]
    visited.add(rope[-1])

    for line in moves:
        direct, steps = line.split(" ")
        head_step = DIRECTIONS[direct]
        for _ in range(int(steps)):
            rope[0] = rope[0][0] + head_step[0], rope[0][1] + head_step[1]
            for chain in range(1, chains):
                if move := calc_move(rope[chain - 1], rope[chain]):
                    rope[chain] = rope[chain][0] + move[0], rope[chain][1] + move[1]
                else:
                    break
            visited.add(rope[-1])

    return len(visited)


if __name__ == "__main__":
    input_lines = get_input_lines()

    print(f"part_a: {count(input_lines, 2)}")
    print(f"part_b: {count(input_lines, 10)}")
