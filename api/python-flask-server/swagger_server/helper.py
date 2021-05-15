import pandas as pd
from amortization.schedule import amortization_schedule


def annualized_analysis(cash, value, rent, rate, term, year_built, sqft, tax, hoa=0, top=None):
    # Initialize empty dictionary of UI requested values
    values = {
        'year': [],
        'mortgage': [],
        'rent': [],
        'equity': [],
        'repair': [],
        'tax': [],
        'vacancy': [],
        'insurance': [],
        'hoa': [],
        'cash_flow': [],
        'cash_return': [],
        'mortgage_return': []
    }

    # initialize constant variables
    cur_value = value
    current_equity = cash
    loan = cur_value - cash
    year = 0
    cur_year = 2020
    cur_top = 0
    total_principal = 0
    insurance = 0.00075 * value

    for number, amount, _, principal, _ in amortization_schedule(loan, rate / 12, term * 12):
        total_principal += principal
        if number % 12 == 0:
            # Initial appreciations
            current_equity += value*.02 + total_principal
            value *= 1.02
            cash_flow = rent * 12 - (amount * 12 + (cur_year - year_built) / 100 * sqft + tax * 12 + insurance + hoa)
            year += 1

            # Set values
            values['hoa'].append(hoa*12)
            values['insurance'].append(insurance)
            values['year'].append(year)
            values['mortgage'].append(amount * 12)
            values['rent'].append(rent * 12)
            values['equity'].append(current_equity)
            values['repair'].append((cur_year - year_built) / 100 * sqft)
            values['tax'].append(tax * 12)
            values['vacancy'].append(rent)
            values['cash_flow'].append(cash_flow)
            values['cash_return'].append(cash_flow / cash)
            values['mortgage_return'].append(current_equity / cash - 1)

            # Post year appreciations
            rent *= 1.02
            tax *= 1.02
            cur_year += 1
            total_principal = 0
            cur_top += 1
            if top is not None and cur_top == top:
                break

    return pd.DataFrame(values)


def get_raw_score(row):
    interest_rate = .03
    payment_rate = (float(interest_rate) / 100 / 12 * (1 + float(interest_rate) / 100 / 12) ** 360) / (
                (1 + float(interest_rate) / 100 / 12) ** 360 - 1)
    cash_flow = row.rent - (payment_rate * row.price * .75 + row.tax + (2020-row.year_built)/100*row.sqft/12 + 0.00075 * row.price/12)
    return cash_flow/row.cash