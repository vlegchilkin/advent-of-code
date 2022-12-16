import time as timer
from typing import Optional
import networkx as nx

from aoc_2022 import Input


def f(src_valve, time, time_next: Optional[int]) -> int:
    if not closed_valves:
        return 0
    best = f(0, time_next, None) if time_next else 0

    for dst_valve in list(closed_valves):
        if time > (ti := costs[src_valve][dst_valve]):
            closed_valves.remove(dst_valve)
            ti = time - ti
            best = max(best, ti * rates[dst_valve] + f(dst_valve, ti, time_next))
            closed_valves.add(dst_valve)

    return best


ttp_template = """\
Valve {{ src }} has flow rate={{ rate | to_int }}; \
{{ ignore(r"tunnel(s)? lead(s)? to valve(s)?") }} {{dst | ORPHRASE | split(", ")}}
"""

if __name__ == "__main__":
    input_data = {d.src: (d.rate, d.dst) for d in Input().get_objects(ttp_template)}
    keys = sorted(input_data)
    rates = [input_data[k][0] for k in keys]
    closed_valves = {valve for valve, rate in enumerate(rates) if rate > 0}

    graph = nx.Graph([(key, dst) for key, value in input_data.items() for dst in value[1]])
    distances = nx.floyd_warshall(graph)
    costs = [[int(distances[k][v]) + 1 for v in keys] for k in keys]

    start_time = timer.time()
    print(f"part_a: {f(0, 30, None)}")
    print(f"part_b: {f(0, 26, 26)}")
    print("--- %s seconds ---" % (timer.time() - start_time))
