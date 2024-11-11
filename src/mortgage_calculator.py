import pandas as pd


class MortgageCalculator:
    MONTHS_PER_YEAR = 12

    def __init__(self, house_cost, term, interest_rate, down_payment_percent=None):
        self.down_payment_amount = house_cost * down_payment_percent if down_payment_percent else 0
        self.loan_amount = house_cost - self.down_payment_amount
        self.loan_term_years = term
        self.interest_rate = interest_rate
        self.monthly_payment = self._calc_monthly_payment(self.loan_amount, self.interest_rate, self.loan_term_years)
        self.annual_payments = self.monthly_payment * MortgageCalculator.MONTHS_PER_YEAR
        self.total_owed = self.monthly_payment * self.loan_term_years * MortgageCalculator.MONTHS_PER_YEAR
        self.amortization_table = self._calc_amortization_table()

    def get_year_one_interest(self):
        return self.amortization_table.loc[self.amortization_table["Year"] == 1, "Interest Payment"].sum()

    def _calc_monthly_payment(self, principal, rate, term):
        # Mortgage Payment Formula
        # Monthly payment = P * r *(1 + r)^n / ((1 + r)^n -1)
        n = MortgageCalculator.MONTHS_PER_YEAR  # monthly payments
        monthly_interest = rate / n
        total_payments = n * term
        numerator = monthly_interest * ((1 + monthly_interest) ** total_payments)
        denominator = ((1 + monthly_interest) ** total_payments) - 1
        monthly_amount = principal * numerator / denominator
        return monthly_amount

    def _calc_amortization_table(self):
        monthly_interest = self.interest_rate / MortgageCalculator.MONTHS_PER_YEAR
        # Build rows first then create df at the end for efficiency
        rows = []
        cur_balance = self.loan_amount
        equity = self.down_payment_amount
        for cur_month in range(self.loan_term_years * MortgageCalculator.MONTHS_PER_YEAR):
            # Use 1 indexing for month and year
            year = 1 + cur_month // MortgageCalculator.MONTHS_PER_YEAR
            month_of_year = 1 + cur_month % MortgageCalculator.MONTHS_PER_YEAR
            interest_payed = cur_balance * monthly_interest
            principal_payed = self.monthly_payment - interest_payed
            equity += principal_payed
            rows.append(
                {"Month": month_of_year, "Year": year, "Balance": cur_balance, "Interest Payment": interest_payed,
                 "Principal Payment": principal_payed, "Equity": equity})
            # Adjust the load balance by interest paid down each month
            cur_balance -= principal_payed
        return pd.DataFrame(rows, columns=["Month", "Year", "Balance", "Interest Payment", "Principal Payment", "Equity"])