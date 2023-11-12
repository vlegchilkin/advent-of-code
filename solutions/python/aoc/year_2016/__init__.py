def assembunny(lines, a=0, b=0, c=0, d=0, out_limit=None, interceptor=None):
    instructions = [(cmd, args.split(" ")) for cmd, _, args in [line.partition(" ") for line in lines]]
    regs = {"a": a, "b": b, "c": c, "d": d}
    out = []

    def get_value(reg_or_int) -> int:
        return regs[reg_or_int] if reg_or_int in regs else int(reg_or_int)

    index = 0
    while 0 <= index < len(instructions):
        cmd, args = instructions[index]
        if interceptor:
            index = interceptor(index, regs, out)

        match cmd:
            case "inc":
                if args[0] in regs:
                    regs[args[0]] += 1
            case "dec":
                if args[0] in regs:
                    regs[args[0]] -= 1
            case "cpy":
                if args[1] in regs:
                    regs[args[1]] = get_value(args[0])
            case "jnz":
                if get_value(args[0]):
                    index += get_value(args[1]) - 1
            case "tgl":
                value = get_value(args[0])
                _index = index + value
                if 0 <= _index < len(instructions):
                    _cmd, _args = instructions[_index]
                    if len(_args) == 1:
                        instructions[_index] = ("dec" if _cmd == "inc" else "inc", _args)
                    else:
                        instructions[_index] = ("cpy" if _cmd == "jnz" else "jnz", _args)
            case "out":
                out.append(get_value(args[0]))
                if out_limit and len(out) == out_limit:
                    break

        index += 1

    return regs, out
