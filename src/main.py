import pandas as pd
from tax_calculator import FederalTaxCalculator, StateTaxCalculator, FilingStatus


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
        self.loan_amount = house_cost - down_payment_amount
        self.loan_term_years = term
        # TODO validate < 1
        self.interest_rate = interest_rate
        self.monthly_payment = self._calc_monthly_payment(self.loan_amount, self.interest_rate, self.loan_term_years)
        self.annual_payments = self.monthly_payment * MONTHS_PER_YEAR
        self.total_owed = self.monthly_payment * self.loan_term_years * MONTHS_PER_YEAR

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

    def calc_ammortization_table(self):
        monthly_interest = self.interest_rate / MONTHS_PER_YEAR
        print(monthly_interest)
        # TODO think about index to use, maybe month (cumulative)
        df = pd.DataFrame(columns=["Month", "Year", "Balance", "Interest Payment", "Principal Payment"])
        # Build rows of df and concat at the end for efficiency
        rows = []
        cur_balance = self.loan_amount
        for cur_month in range(self.loan_term_years * MONTHS_PER_YEAR):
            # Use 1 indexing for month and year
            year = 1 + cur_month // MONTHS_PER_YEAR
            month_of_year = 1 + cur_month % MONTHS_PER_YEAR
            interest_payed = cur_balance * monthly_interest
            principal_payed = self.monthly_payment - interest_payed
            rows.append(
                {"Month": month_of_year, "Year": year, "Balance": cur_balance, "Interest Payment": interest_payed,
                 "Principal Payment": principal_payed})
            # Adjust the load balance by interest paid down each month
            cur_balance -= principal_payed
        self.ammortization_table = pd.concat([df, pd.DataFrame(rows)])
        return self.ammortization_table

    def get_year_one_interest(self):
        # TODO check if the table is null and call method if it is
        return self.ammortization_table.loc[self.ammortization_table["Year"] == 1, "Interest Payment"].sum()


if __name__ == "__main__":
    home_cost = 750_000  # TODO handle down payment deduction
    mortgage_calc = MortgageCalculator(home_cost, 30, 0.05, 0, 0)

    # print(mortgage_calc.total_owed)
    print(mortgage_calc.calc_ammortization_table())
    year_one_interest = mortgage_calc.get_year_one_interest()
    print(year_one_interest)
    # Plot table
    # Calc cumulative principal
    # Calc interest vs. principal percent by month
    # Calc aggregate values by year
    # Calc tax savings
    filing_status = FilingStatus.SINGLE
    gross_income = 200_000
    above_line_deductions = 0
    itemized_deductions = 0
    fed_tax_calc = FederalTaxCalculator(filing_status, gross_income, above_line_deductions, itemized_deductions)
    # TODO calc state income tax
    ny_tax_calc = StateTaxCalculator("NY", filing_status, gross_income, above_line_deductions, itemized_deductions)
    property_tax = ny_tax_calc.calc_property_tax(home_cost)
    state_income_tax, marginal_rate = ny_tax_calc.calc_income_taxes_without_mortgage()
    total_state_tax = property_tax + state_income_tax
    print(property_tax, state_income_tax)
    taxes_wo_mortgage, marg_rate_wo = fed_tax_calc.calc_taxes_without_mortgage()
    taxes_w_mortgage, marg_rate_w = fed_tax_calc.calc_taxes_with_mortgage(home_cost, year_one_interest, total_state_tax)
    tax_savings = taxes_wo_mortgage - taxes_w_mortgage
    savings_per_month = tax_savings / 12
    print(taxes_wo_mortgage, taxes_w_mortgage, tax_savings, savings_per_month)

    # Calc net cost for year 1
    # Calc net cost over time
