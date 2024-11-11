import pandas as pd
# TODO figure out where to put this
MONTHS_PER_YEAR = 12


class MortgageCalculator():

    # TODO add type hinting, comments
    # optional fields
    def __init__(self, house_cost, term, interest_rate, down_payment_percent, down_payment_amount=0):
        # TODO validate only one of down payment percent or amount is defined

        if down_payment_percent:
            # TODO validate percent is a fraction < 1
            down_payment_amount = house_cost * down_payment_percent
        # TODO validate > 0
        self.down_payment_amount = down_payment_amount
        self.loan_amount = house_cost - down_payment_amount
        self.loan_term_years = term
        # TODO validate < 1
        self.interest_rate = interest_rate
        self.monthly_payment = self._calc_monthly_payment(self.loan_amount, self.interest_rate, self.loan_term_years)
        self.annual_payments = self.monthly_payment * MONTHS_PER_YEAR
        self.total_owed = self.monthly_payment * self.loan_term_years * MONTHS_PER_YEAR
        self.amortization_table = self._calc_amortization_table()

    # TODO consider making static
    def _calc_monthly_payment(self, principal, rate, term):
        # Mortgage Payment Formula
        # Monthly payment = P * r *(1 + r)^n / ((1 + r)^n -1)
        n = MONTHS_PER_YEAR  # monthly payments
        monthly_interest = rate / n
        total_payments = n * term
        numerator = monthly_interest * ((1 + monthly_interest) ** total_payments)
        denominator = ((1 + monthly_interest) ** total_payments) - 1
        monthly_amount = principal * numerator / denominator
        return monthly_amount

    def _calc_amortization_table(self):
        monthly_interest = self.interest_rate / MONTHS_PER_YEAR
        # TODO think about index to use, maybe month (cumulative)
        # Build rows first then create df at the end for efficiency
        rows = []
        cur_balance = self.loan_amount
        equity = self.down_payment_amount
        for cur_month in range(self.loan_term_years * MONTHS_PER_YEAR):
            # Use 1 indexing for month and year
            year = 1 + cur_month // MONTHS_PER_YEAR
            month_of_year = 1 + cur_month % MONTHS_PER_YEAR
            interest_payed = cur_balance * monthly_interest
            principal_payed = self.monthly_payment - interest_payed
            equity += principal_payed
            rows.append(
                {"Month": month_of_year, "Year": year, "Balance": cur_balance, "Interest Payment": interest_payed,
                 "Principal Payment": principal_payed, "Equity": equity})
            # Adjust the load balance by interest paid down each month
            cur_balance -= principal_payed
        return pd.DataFrame(rows, columns=["Month", "Year", "Balance", "Interest Payment", "Principal Payment", "Equity"])

    def get_year_one_interest(self):
        # TODO check if the table is null and call method if it is
        return self.amortization_table.loc[self.amortization_table["Year"] == 1, "Interest Payment"].sum()
