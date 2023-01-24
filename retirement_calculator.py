import numpy as np

import inflation_calculator
import accumulated_interest_calculator


def retirement_calculator(expected_monthly_salary: float,
                          current_salary: float,
                          inflation_rate: float,
                          salary_inflation_rate: float,
                          period: int,
                          current_saving: float,
                          interest_rate: float):
    breathing_room = 0.25 * interest_rate
    yearly_salary = 12 * expected_monthly_salary
    inflated_salary = inflation_calculator.inflation_calculator(yearly_salary, inflation_rate, period)[-1]
    required_investment = inflated_salary * 100 / (interest_rate - inflation_rate - breathing_room)

    low, high = 0, 100
    percentage_deposit = low + (high - low) / 2

    _, _, accumulated_investments = accumulated_interest_calculator.interest_calculator(current_saving,
                                                                                        current_salary,
                                                                                        period,
                                                                                        interest_rate,
                                                                                        salary_inflation_rate,
                                                                                        percentage_deposit)

    while abs(high - low) > 0.5 and \
            abs(accumulated_investments[-1] - required_investment) / required_investment > 0.01:
        if accumulated_investments[-1] < required_investment:
            low = percentage_deposit
            percentage_deposit = low + (high - low) / 2
        else:
            high = percentage_deposit
            percentage_deposit = low + (high - low) / 2

        _, _, accumulated_investments = accumulated_interest_calculator.interest_calculator(current_saving,
                                                                                            current_salary,
                                                                                            period,
                                                                                            interest_rate,
                                                                                            salary_inflation_rate,
                                                                                            percentage_deposit)

    return inflated_salary / 12, accumulated_investments, required_investment, percentage_deposit
