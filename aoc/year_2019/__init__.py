from typing import List


def intcode_computer(memory, inp: List | None = None) -> List:
    def parse_modes(modes):
        flags = str(modes).zfill(3)[::-1]
        return list(map(int, flags))

    def at_offset(offset):
        return memory[pos + offset]

    def param(index):
        value, mode = at_offset(index), param_modes[index - 1]
        match mode:
            case 0:
                return memory[value]
            case 1:
                return value
            case _:
                raise ValueError(f"Undefined mode {mode}")

    pos, inp_pos, out = 0, 0, []
    while pos < len(memory):
        param_modes, op_code = parse_modes(memory[pos] // 100), memory[pos] % 100

        match op_code:
            case 1:  # add
                memory[at_offset(3)] = param(1) + param(2)
                pos += 4
            case 2:  # mul
                memory[at_offset(3)] = param(1) * param(2)
                pos += 4
            case 3:  # input
                memory[at_offset(3)] = inp[pos]
                pos, inp_pos = pos + 2, inp_pos + 1
            case 4:  # output
                out.append(param(1))
                pos += 2
            case 5:  # jump-if-true
                pos = param(2) if param(1) != 0 else pos + 3
            case 6:  # jump-if-false
                pos = param(2) if param(1) == 0 else pos + 3
            case 7:  # less than
                memory[at_offset(3)] = int(param(1) < param(2))
                pos += 4
            case 8:  # equals
                memory[at_offset(3)] = int(param(1) == param(2))
                pos += 4
            case 99:
                break
            case _:
                raise ValueError()
    return out
