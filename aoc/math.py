import operator
from functools import reduce

INT_OPER = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.floordiv,
    "%": operator.mod,
}


def factors(n):
    return set(reduce(list.__add__, ([i, n // i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))
