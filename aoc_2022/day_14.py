from aoc_2022 import Input, Spacer, Direction

DIRECTIONS = [Direction.SOUTH, Direction.SOUTH_WEST, Direction.SOUTH_EAST]


def drop(pos, row_limit):
    if a[pos]:
        return False

    while next_pos := next(spacer.get_links(pos, test=lambda p: not a[p] and p[0] <= row_limit), None):
        pos = next_pos

    if pos[0] < row_limit:
        a[pos] = 2
        return True


if __name__ == "__main__":
    lines = Input().get_lines()
    spacer = Spacer(1000, 1000, default_directions=DIRECTIONS)
    a = spacer.new_array(0)
    max_row = 0
    for line in lines:
        points = [[int(x) for x in reversed(step.split(","))] for step in line.split(" -> ")]
        for i in range(1, len(points)):
            s, t = sorted([points[i-1], points[i]])
            a[s[0]:t[0] + 1, s[1]:t[1] + 1] = 1
            max_row = max(max_row, t[0])

    source = (0, 500)
    floor = max_row + 2
    a[floor, ] = 1

    count = 0
    while drop(source, max_row):
        count += 1
    print(f"part_a: {count}")

    while drop(source, floor):
        count += 1
    print(f"part_b: {count}")
