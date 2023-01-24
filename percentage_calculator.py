import math

import inflation_calculator


def percentage_calculator(end_amount: float,
                          start_amount: float,
                          period: int):
    rate = (math.log(end_amount / start_amount) / period) * 100
    accumulated_amount = inflation_calculator.inflation_calculator(start_amount,
                                                                   rate,
                                                                   period)

    return rate, accumulated_amount
