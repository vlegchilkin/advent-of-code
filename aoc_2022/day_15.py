from aoc_2022 import Input, dist


def find_x_areas(y):
    areas = []
    for s in sensors:
        if (delta_x := s[1] - abs(s[0][1] - y)) >= 0:
            areas.append((s[0][0] - delta_x, s[0][0] + delta_x))
    return sorted(areas)


def find_blind_zones(y) -> list[(int, int)]:
    areas = find_x_areas(y)
    max_x = areas[0][1]
    result = []
    for area in areas[1:]:
        if max_x < area[0]:
            result.append((max_x + 1, area[0] - 1))
        max_x = max(max_x, area[1])
    return result


ttp_template = """\
Sensor at x={{ sx | to_int }}, y={{ sy | to_int }}: closest beacon is at x={{ bx | to_int }}, y={{ by | to_int }}
"""

if __name__ == "__main__":
    data = [[(r.sx, r.sy), (r.bx, r.by)] for r in Input().get_objects(ttp_template)]
    sensors = [(d[0], dist(*d)) for d in data]

    part_a_y = 2000000  # 10
    x_areas = find_x_areas(part_a_y)
    part_a = x_areas[-1][1] - x_areas[0][0] + 1
    part_a -= len(set([d[1] for d in data if d[1][1] == part_a_y]))
    print(f"part_a: {part_a}")

    for i in range(0, 4000000):
        if blind_zones := find_blind_zones(i):
            print(f"part_b: {blind_zones[0][0] * 4000000 + i}")
            break
