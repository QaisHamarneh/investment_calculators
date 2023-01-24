import math

import numpy as np


def inflation_calculator(amount: float,
                         inflation_rate: float,
                         years: int):
    amounts = [amount]
    for i in range(1, years + 1):
        amounts.append(amounts[i - 1] * math.exp(inflation_rate / 100))

    return np.array(amounts)
