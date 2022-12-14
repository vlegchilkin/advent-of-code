from aoc_2022 import Input

if __name__ == "__main__":
    input_lines = Input().get_lines()

    timeline = [1]
    for line in input_lines:
        timeline.append(timeline[-1])
        if line != "noop":
            timeline.append(timeline[-1] + (int(line.split(" ")[1])))

    cycles = [20 + i * 40 for i in range(6)]
    part_a = sum([timeline[c - 1] * c for c in cycles])
    print(f"part_a: {part_a}")

    crt = [[], [], [], [], [], []]
    for i in range(40 * 6):
        pixel = "#" if i % 40 in (timeline[i] - 1, timeline[i], timeline[i] + 1) else "."
        crt[i // 40].append(pixel)

    print("part_b:")
    print("\n".join([" ".join(line) for line in crt]))
