import math

APPROXIMATION_CONSTANT = 1e-3


def is_close(number1, number2):
    return math.isclose(number1, number2, abs_tol=APPROXIMATION_CONSTANT)
