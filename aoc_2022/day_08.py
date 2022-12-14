from itertools import product

from aoc_2022 import Input


def see_side(x_list, y_list, height) -> (int, bool):
    trees = 0
    side_view = False
    for x, y in product(x_list, y_list):
        trees += 1
        if forest[x][y] >= height:
            break
    else:
        side_view = True
    return trees, side_view


def look_around(x, y) -> (int, bool):
    n_trees, n_side_view = see_side(reversed(range(x)), [y], forest[x][y])
    s_trees, s_side_view = see_side(range(x + 1, n), [y], forest[x][y])
    w_trees, w_side_view = see_side([x], reversed(range(y)), forest[x][y])
    e_trees, e_side_view = see_side([x], range(y + 1, m), forest[x][y])

    return n_trees * s_trees * w_trees * e_trees, n_side_view | s_side_view | w_side_view | e_side_view


if __name__ == "__main__":
    forest = Input().get_lines()
    n = len(forest)
    m = len(forest[0])

    part_b = 0
    part_a = 0
    for i, j in product(range(n), range(m)):
        tree_factor, side_visible = look_around(i, j)
        if side_visible:
            part_a += 1
        part_b = max(part_b, tree_factor)

    print(f"Part A: {part_a}")
    print(f"Part B: {part_b}")
