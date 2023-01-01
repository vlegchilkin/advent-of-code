from numbers import Complex


def split_to_steps(vector: Complex) -> tuple[Complex, int]:
    if vector == 0:
        return vector, 0

    m = int(max(abs(vector.real), abs(vector.imag)))
    return vector / m, m
