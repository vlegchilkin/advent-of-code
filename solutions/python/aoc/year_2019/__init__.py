from typing import List


class IntcodeComputer:
    def __init__(self, instructions):
        self.memory = {}
        for i, value in enumerate(instructions):
            self.memory[i] = value
        self.pos = 0
        self.relative_base = 0

    def run(self, inp: List | None = None) -> List:
        def parse_modes(modes):
            flags = str(modes).zfill(3)[::-1]
            return list(map(int, flags))

        def ref(index):
            param_address = self.pos + index
            mode = param_modes[index - 1]
            match mode:
                case 0:
                    return self.memory[param_address]
                case 1:
                    return param_address
                case 2:
                    return self.relative_base + self.memory[param_address]
                case _:
                    raise ValueError(f"Undefined mode {mode}")

        def param(index):
            return self.memory[ref(index)]

        inp_pos, out = 0, []
        while self.pos in self.memory:
            param_modes, op_code = parse_modes(self.memory[self.pos] // 100), self.memory[self.pos] % 100

            match op_code:
                case 1:  # add
                    self.memory[ref(3)] = param(1) + param(2)
                    self.pos += 4
                case 2:  # mul
                    self.memory[ref(3)] = param(1) * param(2)
                    self.pos += 4
                case 3:  # input
                    if not inp or inp_pos == len(inp):
                        return out
                    self.memory[ref(1)] = inp[inp_pos]
                    self.pos, inp_pos = self.pos + 2, inp_pos + 1
                case 4:  # output
                    out.append(param(1))
                    self.pos += 2
                case 5:  # jump-if-true
                    self.pos = param(2) if param(1) != 0 else self.pos + 3
                case 6:  # jump-if-false
                    self.pos = param(2) if param(1) == 0 else self.pos + 3
                case 7:  # less than
                    self.memory[ref(3)] = int(param(1) < param(2))
                    self.pos += 4
                case 8:  # equals
                    self.memory[ref(3)] = int(param(1) == param(2))
                    self.pos += 4
                case 9:  # adjusts the relative base
                    self.relative_base += param(1)
                    self.pos += 2
                case 99:
                    break
                case _:
                    raise ValueError()
        return out
