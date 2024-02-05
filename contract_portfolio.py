import pandas as pd
import numpy as np
from portfolio import Portfolio  # Assuming the abstract base class is in portfolio.py
from contract import Contract  # Assuming the Contract class is defined in contract.py

contract_symbols = ['6A', '6C', '6S', 'KC', 'HG', 'ZC', 'CT', '6E', 'GF', 'FCE', 'SCN', '6B', 'GC', 'KE',
 '6J', 'HE', 'LE', '6M', 'FDAX', 'YM', 'RTY', 'FSMI', 'WBS', 'NQ', 'SI', '6N', 'PL',
 'RB', 'LRC', 'ZR', 'ES', 'ZM', 'ZS', 'ZL', 'SB', 'UB', 'ZN', 'VX', 'ZW', 'LSU']


class ContractPortfolio(Portfolio):
    def __init__(self, holdings=None):
        super().__init__(contract_symbols, holdings)

    def initialize_components(self):
        """
        Initialize Contract objects for each symbol in the portfolio.

        :return: A list of Contract objects
        """
        contracts = []
        index = 0
        for symbol in self._symbol_list:
            # Retrieve the number of contracts held for the symbol; default is 1
            num_contracts_held = self._holdings.get(symbol, 1)
            # Create and add Contract objects to the list
            index += 1
            for _ in range(num_contracts_held):
                contracts.append(Contract(symbol))
                print(f"Contract {index} / {len(contract_symbols)} ({symbol}) added to the portfolio.")
            if index == 3:
                break
        return contracts

    def aggregate_returns(self):
        """
        Aggregate returns from each contract in the portfolio.
        This method assumes that each Contract object has a 'get_returns' method
        that returns a DataFrame with a 'Return' column.

        :return: A pandas DataFrame containing the aggregated returns
        """
        # List to hold '1 + Return' columns from each contract's DataFrame
        one_plus_return_cols = []

        for contract in self._components:
            contract_returns_df = contract.get_returns()
            contract_returns_df.replace([np.inf, -np.inf], np.nan, inplace=True)
            contract_returns_df.dropna(inplace=True)

            # Verify the '1 + Return' column exists
            if '1 + Return' in contract_returns_df.columns:
                one_plus_return_cols.append(contract_returns_df['1 + Return'])
            else:
                print(f"Contract {contract.get_symbol()} DataFrame missing '1 + Return' column.")

        # Concatenate all '1 + Return' columns along the column axis using inner join
        all_returns = pd.concat(one_plus_return_cols, axis=1, join='inner')

        # Calculate the product of '1 + Return' across all contracts (row-wise)
        portfolio_1_plus_return = all_returns.prod(axis=1, skipna=False)

        # Create portfolio DataFrame
        portfolio_df = pd.DataFrame(index=all_returns.index)
        portfolio_df['Portfolio Return'] = portfolio_1_plus_return - 1

        return portfolio_df.dropna()

# Example usage:
# Assuming list_of_symbols is a list of contract symbols
# contract_portfolio = ContractPortfolio(list_of_symbols)
# print(contract_portfolio.get_returns())
