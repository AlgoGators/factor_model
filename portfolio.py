import pandas as pd
import numpy as np
from contract import Contract
from factor import Factor
import os
import glob

list_of_symbols = ['6A', '6B', '6C', '6E', '6J', '6M', '6N', '6S', 'AFB', 'AWM', 'BAX', 'BRN', 'CGB', 'CL', 'CT', 'DC',
                    'DX', 'ES', 'EUA', 'FBTP', 'FCE', 'FDAX', 'FESX', 'FGBL', 'FGBM', 'FGBS', 'FGBX', 'FSMI', 'FTDX',
                    'GAS', 'GC', 'GD', 'GF', 'GWM', 'HE', 'HG', 'HO', 'HSI', 'HTW', 'KC', 'KE', 'KOS', 'LBS', 'LCC',
                    'LEU', 'LE', 'LFT', 'LLG', 'LRC', 'LSU', 'LWB', 'MHI', 'MWE', 'NG', 'NIY', 'NKD', 'NQ', 'OJ', 'PA',
                    'PL', 'RB', 'RS', 'RTY', 'SB', 'SCN', 'SI', 'SJB', 'SNK', 'SSG', 'SXF', 'UB', 'VX', 'WBS', 'YAP',
                    'YIB', 'YIR', 'YM', 'YXT', 'YYT', 'ZB', 'ZC', 'ZF', 'ZL', 'ZM', 'ZN', 'ZO', 'ZQ', 'ZR', 'ZS',
                    'ZT', 'ZW']


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


"""
# Instantiate Portfolio with equal weights by default
# test_port = Portfolio(list_of_symbols)
# print(test_port.get_returns())
"""

