from dataclasses import dataclass
from enum import Enum, auto


class FilingStatus(Enum):
    SINGLE = auto()
    HEAD_OF_HOUSEHOLD = auto()
    MARRIED_JOINTLY = auto()
    MARRIED_SEPARATELY = auto()


@dataclass
class Bracket:
    tax_rate: float
    start_income: int


class BaseTaxCalculator:
    def __init__(self, std_ded_map: dict[FilingStatus, int], brackets: dict[FilingStatus, list[Bracket]]):
        self._std_ded_map = std_ded_map
        self._brackets = brackets

    def get_standard_deduction(self, filing_status: FilingStatus):
        return self._std_ded_map[filing_status]

    # TODO document
    def _calc_taxes(self, filing_status: FilingStatus, taxable_income: int) -> (float, float):
        marginal_rate = 0
        total_tax = 0
        remaining_income = taxable_income  # It is possible for taxable income to be 0, don't want to go negative
        # Iterate over the brackets in reverse and adjust the remaining income to be taxed. Determine the income
        # that is taxed at the current rate and calculate the tax owed for the current bracket.
        for bracket in reversed(self._brackets[filing_status]):
            if remaining_income > bracket.start_income:
                # The marginal tax rate will always be the highest rate you are taxed at
                marginal_rate = max(marginal_rate, bracket.tax_rate)
                income_in_bracket = remaining_income - bracket.start_income
                total_tax += income_in_bracket * bracket.tax_rate
                remaining_income = bracket.start_income
        return total_tax, marginal_rate


class FederalTaxCalculator(BaseTaxCalculator):
    # Maximum State and Local Taxes (SALT) that can be deducted from federal income
    _SALT_TAX_LIMIT = 10_000
    # Maximum mortgage whose interest can be deducted.
    MORTGAGE_LIMIT = {FilingStatus.SINGLE: 750_000,
                       FilingStatus.HEAD_OF_HOUSEHOLD: 750_000,
                       FilingStatus.MARRIED_JOINTLY: 750_000,
                       FilingStatus.MARRIED_SEPARATELY: 375_000}

    def __init__(self, filing_status: FilingStatus, gross_income: int, above_line_deductions: int,
                 itemized_deductions: int):
        # TODO fill out other brackets
        super().__init__(
            {FilingStatus.SINGLE: 14600, FilingStatus.HEAD_OF_HOUSEHOLD: 21900, FilingStatus.MARRIED_JOINTLY: 29200,
             FilingStatus.MARRIED_SEPARATELY: 14600},
            {FilingStatus.SINGLE: [Bracket(0.1, 0), Bracket(0.12, 11_600), Bracket(0.22, 47_150),
                                   Bracket(0.24, 100_500),
                                   Bracket(0.32, 191_950), Bracket(0.35, 243_725), Bracket(0.37, 609_350)]
             })
        # TODO validate filing status and throw unsupported exception for yet to be implemented
        self.filing_status = filing_status
        self.gross_income = gross_income
        self.above_line_deductions = above_line_deductions
        self.itemized_deductions = itemized_deductions

    def calc_taxes_without_mortgage(self, salt_taxes=0):
        net_income = self.gross_income - self.above_line_deductions
        std_ded = self.get_standard_deduction(self.filing_status)
        deductible_salt_taxes = min(FederalTaxCalculator._SALT_TAX_LIMIT, salt_taxes)
        total_deductions = deductible_salt_taxes + self.itemized_deductions
        # Many people won't have enough deductions to go above the standard deduction, take the higher of the values
        additional_deductions = max(std_ded, total_deductions)
        net_income -= additional_deductions
        net_income = max(net_income, 0)
        return self._calc_taxes(self.filing_status, net_income)

    def calc_taxes_with_mortgage(self, loan_amount, annual_interest, salt_taxes):
        # Figure out the amount of mortgage interest that is deductible
        loan_limit = FederalTaxCalculator.MORTGAGE_LIMIT[self.filing_status]
        deductible_interest = annual_interest * (min(loan_limit, loan_amount) / loan_limit)
        # Figure out the salt taxes that count
        # Salt limit is the same where filing jointly or separately, marriage penalty
        deductible_salt_taxes = min(FederalTaxCalculator._SALT_TAX_LIMIT, salt_taxes)
        # Look at the new below the line deductions
        total_deductions = deductible_interest + deductible_salt_taxes + self.itemized_deductions
        std_ded = self.get_standard_deduction(self.filing_status)
        additional_deductions = max(total_deductions, std_ded)
        net_income = self.gross_income - self.above_line_deductions - additional_deductions
        # Look at new taxes owed and marginal rate
        return self._calc_taxes(self.filing_status, net_income)


class StateTaxCalculator(BaseTaxCalculator):
    _PROPERTY_TAX_EST = {"NY": 0.014}

    _STD_DEDUCTIONS = {
        "NY": {FilingStatus.SINGLE: 8_000, FilingStatus.HEAD_OF_HOUSEHOLD: 11_200, FilingStatus.MARRIED_JOINTLY: 16_050,
               FilingStatus.MARRIED_SEPARATELY: 8_000}}

    _TAX_BRACKETS = {"NY": {FilingStatus.SINGLE: [Bracket(0.04, 0), Bracket(0.045, 8_500), Bracket(0.0525, 11_700),
                                                  Bracket(0.055, 13_900), Bracket(0.06, 80_650),
                                                  Bracket(0.0685, 215_400),
                                                  Bracket(0.0965, 1_077_550), Bracket(0.103, 5_000_000),
                                                  Bracket(0.109, 25_000_000)]}
                     }

    _MORTGAGE_LIMIT = {"NY": FederalTaxCalculator.MORTGAGE_LIMIT}

    def __init__(self, state: str, filing_status: FilingStatus, gross_income: int, above_line_deductions: int,
                 itemized_deductions: int):
        # TODO validate, make all caps
        self.state = state
        super().__init__(
            std_ded_map=StateTaxCalculator._STD_DEDUCTIONS[self.state],
            brackets=StateTaxCalculator._TAX_BRACKETS[self.state]
        )
        self.filing_status = filing_status
        self.gross_income = gross_income
        self.above_line_deductions = above_line_deductions
        self.itemized_deductions = itemized_deductions

    # TODO def, property taxes are typically defined by county, currently uses an estimate, optional parameter allows custom rate
    # TODO think about adding exemptions or deductions
    def calc_property_tax(self, home_value, tax_rate=None):
        tax_rate = tax_rate if tax_rate is not None else StateTaxCalculator._PROPERTY_TAX_EST[self.state]
        return tax_rate * home_value

    def calc_income_taxes_without_mortgage(self):
        net_income = self.gross_income - self.above_line_deductions
        std_ded = self.get_standard_deduction(self.filing_status)
        # Many people won't have enough deductions to go above the standard deduction, take the higher of the values
        additional_deductions = max(std_ded, self.itemized_deductions)
        net_income -= additional_deductions
        net_income = max(net_income, 0)
        return self._calc_taxes(self.filing_status, net_income)

    def calc_income_taxes_with_mortgage(self, loan_amount, annual_interest):
        # Figure out the amount of mortgage interest that is deductible
        loan_limit = StateTaxCalculator._MORTGAGE_LIMIT[self.state][self.filing_status]
        deductible_interest = annual_interest * (min(loan_limit, loan_amount) / loan_limit)
        # Look at the new below the line deductions
        total_deductions = deductible_interest + self.itemized_deductions
        std_ded = self.get_standard_deduction(self.filing_status)
        additional_deductions = max(total_deductions, std_ded)
        net_income = max(self.gross_income - self.above_line_deductions - additional_deductions, 0)
        # Look at new taxes owed and marginal rate
        return self._calc_taxes(self.filing_status, net_income)
