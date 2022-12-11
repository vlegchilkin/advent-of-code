from aoc_2022 import Input

if __name__ == "__main__":
    pairs = Input().get_lists("{{a0|to_int}}-{{a1|to_int}},{{b0|to_int}}-{{b1|to_int}}")

    overlap = intersect = 0
    for a_, _a, b_, _b in pairs:
        overlap += (a_ <= b_ and _b <= _a) or (b_ <= a_ and _a <= _b)
        intersect += (a_ <= b_ <= _a) or (b_ <= a_ <= _b)

    print(f"part_a: {overlap}")
    print(f"part_b: {intersect}")
