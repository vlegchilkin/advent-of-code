from aoc_2022 import get_input_lines


if __name__ == "__main__":
    capacities = []
    sums = 0

    for line in get_input_lines(0):
        if line:
            sums += int(line)
        else:
            capacities.append(sums)
            sums = 0
    capacities.append(sums)

    top3 = sorted(capacities, reverse=True)[:3]
    print(f"MAX: {top3[0]}")
    print(f"TOP3: {top3}")
    print(f"TOP3_SUM: {sum(top3)}")
