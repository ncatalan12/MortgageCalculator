from tax_calculator import FederalTaxCalculator, StateTaxCalculator, FilingStatus
from mortgage_calculator import MortgageCalculator
import matplotlib.pyplot as plt

if __name__ == "__main__":
    home_cost = 750_000  # TODO handle down payment deduction
    mortgage_calc = MortgageCalculator(home_cost, 30, 0.05, 0, 0)

    am_tb = mortgage_calc.amortization_table
    # "Interest Payment", "Principal Payment"
    # ax = am_tb[["Interest Payment", "Principal Payment"]].plot(kind='line')
    plt.figure()
    plt.plot(am_tb.index, am_tb["Interest Payment"], label="Interest")
    plt.plot(am_tb.index, am_tb["Principal Payment"], label="Principal")
    plt.title("Interest Payments Over Time", fontsize=16)
    plt.xlabel("Month", fontsize=12)
    plt.ylabel("Payment Amount ($)", fontsize=12)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    # plt.show()

    # ax2 = am_tb["Balance"].plot(kind='line')
    # plt.title("Interest Payments Over Time", fontsize=16)
    # plt.xlabel("Month", fontsize=12)
    # plt.ylabel("Payment Amount ($)", fontsize=12)
    # plt.grid(True)
    plt.figure()
    plt.plot(am_tb.index, am_tb["Balance"], label="Balance")
    plt.plot(am_tb.index, am_tb["Equity"], label="Equity")
    plt.title("Equity and Load Balance Over Time", fontsize=16)
    plt.xlabel("Month", fontsize=12)
    plt.ylabel("$", fontsize=12)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # # print(mortgage_calc.total_owed)
    # # print(mortgage_calc.calc_amortization_table())
    # year_one_interest = mortgage_calc.get_year_one_interest()
    # print(year_one_interest)
    # # Plot table
    # # Calc cumulative principal
    # # Calc interest vs. principal percent by month
    # # Calc aggregate values by year
    # # Calc tax savings
    # filing_status = FilingStatus.SINGLE
    # gross_income = 200_000
    # above_line_deductions = 0
    # itemized_deductions = 0
    # fed_tax_calc = FederalTaxCalculator(filing_status, gross_income, above_line_deductions, itemized_deductions)
    # # TODO calc state income tax
    # ny_tax_calc = StateTaxCalculator("NY", filing_status, gross_income, above_line_deductions, itemized_deductions)
    # property_tax = ny_tax_calc.calc_property_tax(home_cost)
    # state_income_tax = ny_tax_calc.calc_income_taxes_without_mortgage()
    # state_income_tax_wo_mortgage = ny_tax_calc.calc_income_taxes_with_mortgage(home_cost, year_one_interest)
    # print(state_income_tax, state_income_tax_wo_mortgage)
    # total_state_tax = property_tax + state_income_tax
    # # print(property_tax, state_income_tax)
    # taxes_wo_mortgage = fed_tax_calc.calc_taxes_without_mortgage(state_income_tax)
    # taxes_w_mortgage = fed_tax_calc.calc_taxes_with_mortgage(home_cost, year_one_interest, total_state_tax)
    # tax_savings = taxes_wo_mortgage - taxes_w_mortgage
    # savings_per_month = tax_savings / 12
    # print(taxes_wo_mortgage, taxes_w_mortgage, tax_savings, savings_per_month)
    #
    # # Calc net cost for year 1
    # # Calc net cost over time
