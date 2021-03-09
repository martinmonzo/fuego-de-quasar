import math

APPROXIMATION_CONSTANT = 1e-3
ROUND_SIGNIFICANT_DECIMALS = 3


def is_close(number1, number2):
    """
    Determine whether two numbers are close to each other. That is, that the
    difference between both is less than or equal to APPROXIMATION_CONSTANT.

    Args:
        - number1 (float)
        - number2 (float)

    Returns:
        bool:
            - True if math.abs(number1 - number2) <= APPROXIMATION_CONSTANT).
            - False otherwise.
    """
    return math.isclose(number1, number2, abs_tol=APPROXIMATION_CONSTANT)
