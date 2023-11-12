import networkx as nx
import pytest

from aoc import Input, get_puzzles, PuzzleData, Solution
from aoc.space import C_NSWE


class Year2018Day20(Solution):
    """2018/20: A Regular Map"""

    def __init__(self, inp: Input):
        self.path = inp.get_lines()[0][1:-1]

    def part_a_b(self):
        start_pos = 0j
        graph = nx.Graph()
        graph.add_node(start_pos)
        it = iter(self.path)

        def recu(poses: set):
            while (d := next(it, None)) is not None:
                while d in C_NSWE:
                    _poses = set()
                    move = C_NSWE[d]
                    for pos in poses:
                        _pos = pos + move
                        graph.add_edge(pos, _pos)
                        _poses.add(_pos)
                    poses = _poses
                    d = next(it, None)

                if d is None:
                    return
                if d == "|":
                    return poses, False
                if d == ")":
                    return poses, True

                x_possible, final = set(), False
                while not final:
                    x_poses, final = recu(poses)
                    x_possible |= x_poses
                poses = x_possible

        recu({start_pos})
        paths = nx.single_source_shortest_path_length(graph, start_pos)

        return max(paths.values()), sum(1 for r in paths.values() if r >= 1000)


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2018Day20)
