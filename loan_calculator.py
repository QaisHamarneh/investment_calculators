import numpy as np


def loan_calculator(loan_amount: float,
                    interest_rate: float,
                    period: int):
    monthly_interest = (interest_rate / 12) / 100
    nr_payments = period * 12
    temp = (1 + monthly_interest) ** nr_payments
    monthly_payment = loan_amount / ((temp - 1) / (monthly_interest * temp))

    principles = [loan_amount]
    interests = [0]
    totals = [loan_amount]
    for i in range(period):
        principle = principles[i]
        interest_sum = 0
        total = totals[i]
        for j in range(1, 13):
            interest = principle * monthly_interest
            principle = principle - (monthly_payment - interest)
            total += monthly_payment
            interest_sum += interest
        principles.append(principle)
        interests.append(interest_sum + interests[i])
        totals.append(total)
    total_amount = monthly_payment * 12 * period

    return total_amount, monthly_payment, np.array(principles), np.array(interests), np.array(totals)


def higher_monthly_payment_calculator(loan_amount: float,
                                      interest_rate: float,
                                      new_monthly_payment: float):
    monthly_interest = (interest_rate / 12) / 100

    years = 0
    months = 0
    principles = [loan_amount]
    interests = [0]
    totals = [0]
    total_amount = loan_amount
    i = 0
    while principles[-1] > 0 and i < 200:
        for j in range(1, 13):
            interest = principles[-1] * monthly_interest
            principles.append(principles[-1] - (new_monthly_payment - interest))
            interests.append(interests[-1] + interest)
            totals.append(totals[-1] + new_monthly_payment)
            if principles[-1] <= 0:
                years = i if j < 12 else i + 1
                months = j if j < 12 else 0
                break
        if principles[-1] <= 0:
            total_amount = totals[-1] + principles[-1]
            break

        i += 1
        if i == 200:
            total_amount = totals[-1] + principles[-1]
            years = i
            break

    return total_amount, years, months, np.array(principles), np.array(interests), np.array(totals)

