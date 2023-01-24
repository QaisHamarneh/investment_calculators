import numpy as np


def interest_calculator(current_saving: float,
                        current_monthly_salary: float,
                        period: int,
                        interest_rate: float,
                        salary_inflation_rate: float,
                        percentage_deposit: float):
    current_yearly_salary = current_monthly_salary * 12
    investment_percentage = percentage_deposit / 100
    monthly_interest_rate = (interest_rate / 12) / 100
    principles = [current_saving]
    interests = [0]
    totals = [current_saving]
    for i in range(1, period + 1):
        monthly_salary = current_yearly_salary / 12
        deposit = 0
        accumulated_interest = 0
        for _ in range(12):
            accumulated_interest += (totals[i - 1] + deposit) * monthly_interest_rate
            deposit += monthly_salary * investment_percentage
        principles.append(principles[i - 1] + deposit)
        totals.append(totals[i - 1] + deposit + accumulated_interest)
        interests.append(interests[i - 1] + accumulated_interest)

        current_yearly_salary *= 1 + (salary_inflation_rate / 100)

    return np.array(principles), np.array(interests), np.array(totals)
