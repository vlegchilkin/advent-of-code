import operator
from functools import reduce

INT_OPERATOR = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.floordiv,
    "%": operator.mod,
}

BOOL_OPERATOR = {
    "<": operator.lt,
    ">": operator.gt,
    ">=": operator.ge,
    "<=": operator.le,
    "!=": operator.ne,
    "==": operator.eq,
}


def factors(n):
    return set(reduce(list.__add__, ([i, n // i] for i in range(1, int(n ** 0.5) + 1) if n % i == 0)))


def ceil_div(a: int, b: int) -> int:
    return -(a // -b)
