import collections
import re

import pytest

from aoc import Input, get_puzzles, PuzzleData, ISolution, parse_with_template

TTP_TEMPLATE = """
<group name="state">
In state {{name}}:
<group name="condition">
  If the current value is {{value|to_int}}:
    - Write the value {{out|to_int}}.
    - Move one slot to the {{move}}.
    - Continue with state {{state}}.
</group>
</group>
"""


class Year2017Day25(ISolution):
    """2017/25: The Halting Problem"""

    def __init__(self, inp: Input):
        it = inp.get_iter()
        self.start_state = re.match(r"^Begin in state (\w+).$", next(it)).groups()[0]
        self.steps = int(re.match(r"^Perform a diagnostic checksum after (\d+) steps.$", next(it)).groups()[0])
        next(it)
        self.states = {}
        for d in parse_with_template("\n".join(it), TTP_TEMPLATE)[0]["state"]:
            for c in d["condition"]:
                self.states[(d["name"], c["value"])] = (c["state"], 1 if c["move"] == "right" else -1, c["out"])

    def part_a(self):
        tape = collections.defaultdict(int)
        state, pos = self.start_state, 0
        for _ in range(self.steps):
            state, move, out = self.states[(state, tape[pos])]
            tape[pos] = out
            pos += move

        return sum(tape.values())


@pytest.mark.parametrize("pd", get_puzzles(), ids=str)
def test_case(pd: PuzzleData):
    pd.check_solution(Year2017Day25)
