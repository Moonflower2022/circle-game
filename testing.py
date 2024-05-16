import math

def left_case(blocker1, blocker2):
    A, B = blocker1
    C, D = blocker2

    if A == C or A == 0 or C == 0:
        print("Error: A must not be equal to C, A must not be zero, and C must not be zero")
        return None, None

    numerator = -math.sqrt(A * C * (A**2 - 2 * A * C + B**2 - 2 * B * D + C**2 + D**2)) - A * D + B * C
    denominator = A - C
    y = numerator / denominator

    inner_expression = math.sqrt(A * C * (A**2 - 2 * A * C + B**2 - 2 * B * D + C**2 + D**2))
    numerator = (A**3 + 2 * B * (inner_expression - C * D) - 2 * D * inner_expression - A**2 * C + A * (B**2 - 2 * B * D - C**2 + D**2) + B**2 * C + C**3 + C * D**2)
    denominator = 2 * (A - C)**2
    x = numerator / denominator

    return (x, y), x

def right_case(blocker1, blocker2):
    A, B = blocker1
    C, D = blocker2

    if (A - C) == 0 or (A - 1) == 0 or (C - 1) == 0:
        print("Error: A - C, A - 1, and C - 1 must not be zero")
        return None, None

    inner_expression = math.sqrt((A - 1) * (C - 1) * (A**2 - 2 * A * C + B**2 - 2 * B * D + C**2 + D**2))
    numerator = (A**3 - 2 * B * inner_expression + 2 * D * inner_expression - A**2 * C + A * B**2 - 2 * A * B * D - A * C**2 + A * D**2 + B**2 * C - 2 * B**2 - 2 * B * C * D + 4 * B * D + C**3 + C * D**2 - 2 * D**2)
    denominator = 2 * (A - C)**2
    x =  numerator / denominator

    inner_expression = math.sqrt((A - 1) * (C - 1) * (A**2 - 2 * A * C + B**2 - 2 * B * D + C**2 + D**2))
    numerator = math.sqrt((A - 1) * (C - 1) * (A**2 - 2 * A * C + B**2 - 2 * B * D + C**2 + D**2)) + A * D + B * (-C) + B - D
    denominator = A - C
    y =  numerator / denominator

    return (x, y), 1 - x 

blocker1 = (0.6, 0.9)
blocker2 = (0.5, 0.1)

print(left_case(blocker1, blocker2))
print(left_case(blocker2, blocker1))

print(right_case(blocker1, blocker2))
print(right_case(blocker2, blocker1))