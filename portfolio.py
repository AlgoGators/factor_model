import pandas as pd
import numpy as np
from contract import Contract
from factor import Factor
import os
import glob


class Portfolio:
    def __init__(self, symbol_list, num_contracts_held=None):
        self._symbol_list = symbol_list

        # Set so we can later adjust weightings - default otherwise is 1 contract per symbol
        self._num_contracts_held = num_contracts_held if num_contracts_held is not None else {symbol: 1 for symbol in
                                                                                              symbol_list}

        self._contracts = self.set_contracts()
        self._contract_returns_df_list = self.set_contract_returns()
        self._returns = self.set_returns()

    def set_returns(self):
        # List to hold '1 + Return' columns from each DataFrame
        one_plus_return_cols = []

        for return_df in self._contract_returns_df_list:
            # Check if '1 + Return' column exists
            if '1 + Return' in return_df.columns:
                one_plus_return_cols.append(return_df['1 + Return'])
            else:
                print(f"DataFrame missing '1 + Return' column: {return_df}")
                # Optionally, handle the missing column case, e.g., continue, add default values, etc.

        # Concatenate all '1 + Return' columns along the column axis using inner join
        all_returns = pd.concat(one_plus_return_cols, axis=1, join='inner')

        # Calculate the product of '1 + Return' across all contracts (row-wise)
        portfolio_1_plus_return = all_returns.prod(axis=1, skipna=False)

        # Create portfolio DataFrame
        portfolio_df = pd.DataFrame(index=all_returns.index)
        portfolio_df['1 + Return'] = portfolio_1_plus_return
        portfolio_df['Return'] = portfolio_1_plus_return - 1

        return portfolio_df

    def get_returns(self):
        # Ensure the returns are aligned and aggregated
        return self._returns

    def set_contracts(self):
        contracts = []
        # index = 3
        for symbol in self._symbol_list:
            num_contracts_held = self._num_contracts_held.get(symbol, 1)
            for _ in range(num_contracts_held):
                contract = Contract(symbol)
                contracts.append(contract)
                print(f'Added {symbol} to portfolio.')
            # index -= 1
            # if index == 0:
            # break
        return contracts

    def set_contract_returns(self):
        returns = []
        for contract in self._contracts:
            contract_returns_df = contract.get_returns()
            returns.append(contract_returns_df)
            print(f'Added {contract.get_symbol()} to portfolio returns.')
        return returns


# Usage of the Portfolio class
# Only using this base path to get list of symbols, can also do it by pulling the names from SQL tables - same for main
# base_path = r'C:\Users\kbott\OneDrive\Desktop\AlgoData\OutputFile\Contract_Data
# list_of_symbols = []
"""
for file_name in os.listdir(base_path):
    if file_name.endswith('_Data.csv'):  # This ensures only the relevant files are considered
        symbol = file_name.replace('&', '').replace('_Data.csv', '')
        list_of_symbols.append(symbol)

# Instantiate Portfolio with equal weights by default
test_port = Portfolio(list_of_symbols)
print(test_port.get_returns())
"""
