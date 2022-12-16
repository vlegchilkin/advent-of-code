import time as timer
from typing import Optional

from aoc_2022 import Input, Graph


def f(src_valve, time, time_next: Optional[int]) -> int:
    if not closed_valves:
        return 0
    best = f(0, time_next, None) if time_next else 0

    for dst_valve in list(closed_valves):
        if time > (ti := costs[src_valve][dst_valve]):
            closed_valves.remove(dst_valve)
            ti = time - ti
            best = max(best, ti * valves[dst_valve] + f(dst_valve, ti, time_next))
            closed_valves.add(dst_valve)

    return best


ttp_template = """\
Valve {{ src }} has flow rate={{ rate | to_int }}; {{ dst | ORPHRASE | split(", ") }}
"""

if __name__ == "__main__":
    input_data = {d.src: (d.rate, d.dst) for d in Input().get_objects(ttp_template)}
    for _, dst in input_data.values():
        dst[0] = dst[0].rpartition(" ")[-1]

    keys = sorted(input_data)
    valves = [input_data[k][0] for k in keys]
    links = {keys.index(k): [(keys.index(d), 1) for d in input_data[k][1]] for k in keys}

    costs = Graph(links).floyd().add_weight(1).to_list()
    closed_valves = {i for i, valve in enumerate(valves) if valve > 0}

    start_time = timer.time()
    print(f"part_a: {f(0, 30, None)}")
    print(f"part_b: {f(0, 26, 26)}")
    print("--- %s seconds ---" % (timer.time() - start_time))
