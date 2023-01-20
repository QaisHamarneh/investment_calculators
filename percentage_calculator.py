import inflation_calculator


def percentage_calculator(end_amount: float,
                          start_amount: float,
                          period: int):
    low, high = 0, 100
    rate = low + (high - low) / 2
    accumulated_amount = inflation_calculator.inflation_calculator(start_amount,
                                                                   rate,
                                                                   period)
    while abs(high - low) > 0.5 and \
            abs(accumulated_amount[-1] - end_amount) / end_amount > 0.001:
        if accumulated_amount[-1] < end_amount:
            low = rate
            rate = low + (high - low) / 2
        else:
            high = rate
            rate = low + (high - low) / 2
        accumulated_amount = inflation_calculator.inflation_calculator(start_amount,
                                                                       rate,
                                                                       period)

    return rate, accumulated_amount
