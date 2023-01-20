import numpy as np


def interest_calculator(initial_amount: float,
                        interest_rate: float,
                        period: int,
                        current_monthly_salary: float,
                        salary_inflation_rate: float,
                        percentage_deposit: float):
    current_yearly_salary = current_monthly_salary * 12
    principles = [initial_amount]
    interests = [0]
    totals = [initial_amount]
    for i in range(1, period + 1):
        monthly_salary = current_yearly_salary / 12
        deposit = 0
        accumulated_interest = 0
        for _ in range(12):
            accumulated_interest += (totals[i - 1] + deposit) * ((interest_rate / 12) / 100)
            deposit += monthly_salary * (percentage_deposit / 100)
        principles.append(principles[i - 1] + deposit)
        totals.append(totals[i - 1] + deposit + accumulated_interest)
        interests.append(interests[i - 1] + accumulated_interest)

        current_yearly_salary = current_yearly_salary + current_yearly_salary * (salary_inflation_rate / 100)

    return np.array(principles), np.array(interests), np.array(totals)