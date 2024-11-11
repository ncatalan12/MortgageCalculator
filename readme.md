Mortgage Calculator
====
Packages for calculating mortgage costs and amortization tables, income taxes and deductions, and potential tax savings.
Includes Jupyter notebook for running experimental calculations and visualizing outputs.

### Notebook Usage
Assumes python is installed in your path.

Run `run_notebook.sh` from terminal. 

This handles venv setup, installation of required packages, and installation of mortgage and tax packages in editable 
mode so that changes can be made iteratively.

### Limitations
This calculator is meant to give an estimate of taxes that apply to the typical filer.
Tax calculations and savings are estimates only, taxes are complicated and vary substantially for individuals.

All tax calculations are for 2024 only. 
Tax brackets change annually and the tax code changes frequently. This calculator may not reflect the latest changes. 

#### Mortgage Interest Deductions
The mortgage interest you pay decreases over time. The tax savings provided use the first year tax savings.
Each subsequent year will have lower interest payments and therefore lower tax savings 
(with the benefit of more equity being built up in the home).

#### State Taxes
Currently only NY state is handled for state taxes. 
Additional states can be added by extending the StateTaxCalculator class.
Property taxes typically vary by county and a state average is used to get an estimate.
