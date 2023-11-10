from typing import List


class IntcodeComputer:
    def __init__(self, memory):
        self.memory = memory
        self.pos = 0

    def run(self, inp: List | None = None) -> List:
        def parse_modes(modes):
            flags = str(modes).zfill(3)[::-1]
            return list(map(int, flags))

        def at_offset(offset):
            return self.memory[self.pos + offset]

        def param(index):
            value, mode = at_offset(index), param_modes[index - 1]
            match mode:
                case 0:
                    return self.memory[value]
                case 1:
                    return value
                case _:
                    raise ValueError(f"Undefined mode {mode}")

        inp_pos, out = 0, []
        while self.pos < len(self.memory):
            param_modes, op_code = parse_modes(self.memory[self.pos] // 100), self.memory[self.pos] % 100

            match op_code:
                case 1:  # add
                    self.memory[at_offset(3)] = param(1) + param(2)
                    self.pos += 4
                case 2:  # mul
                    self.memory[at_offset(3)] = param(1) * param(2)
                    self.pos += 4
                case 3:  # input
                    if not inp or inp_pos == len(inp):
                        return out
                    self.memory[at_offset(1)] = inp[inp_pos]
                    self.pos, inp_pos = self.pos + 2, inp_pos + 1
                case 4:  # output
                    out.append(param(1))
                    self.pos += 2
                case 5:  # jump-if-true
                    self.pos = param(2) if param(1) != 0 else self.pos + 3
                case 6:  # jump-if-false
                    self.pos = param(2) if param(1) == 0 else self.pos + 3
                case 7:  # less than
                    self.memory[at_offset(3)] = int(param(1) < param(2))
                    self.pos += 4
                case 8:  # equals
                    self.memory[at_offset(3)] = int(param(1) == param(2))
                    self.pos += 4
                case 99:
                    break
                case _:
                    raise ValueError()
        return out
