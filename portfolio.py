import pandas as pd
import numpy as np
from contract import Contract
from factor import Factor
import os
import glob


class Portfolio:
    def __init__(self, symbol_list, weights=None):
        self._symbol_list = symbol_list
        self._contracts = self.set_contracts()
        self._returns = self.set_returns()
        # Set equal weights if weights are not provided
        self._weights = weights if weights is not None else np.ones(len(self._contracts)) / len(self._contracts)

    def align_and_aggregate_returns(self):
        # Initialize aligned_returns as None
        aligned_returns = None

        # Joining the return series of all contracts
        for i, contract_returns in enumerate(self._returns):
            if aligned_returns is None:
                aligned_returns = contract_returns.copy()
            else:
                aligned_returns = aligned_returns.join(contract_returns, how='outer', rsuffix=f'_{i}')

        # Handling NaN values using interpolation
        aligned_returns.interpolate(method='linear', inplace=True)

        # Debugging: Check shapes of aligned_returns and weights
        print(f"Shape of aligned_returns: {aligned_returns.shape}")
        print(f"Length of weights: {len(self._weights)}")

        if len(self._weights) != aligned_returns.shape[1]:
            print(f"Adjusting weights to match the number of contracts: {aligned_returns.shape[1]}")
            self._weights = np.ones(aligned_returns.shape[1]) / aligned_returns.shape[1]

        # Aggregating returns with weights
        weighted_aggregated_returns = (aligned_returns * self._weights).sum(axis=1)

        return weighted_aggregated_returns

    def get_returns(self):
        # Ensure the returns are aligned and aggregated
        return self.align_and_aggregate_returns()

    def set_contracts(self):
        contracts = []
        for symbol in self._symbol_list:
            contract = Contract(symbol)
            contracts.append(contract)
            print(f'Added {symbol} to contracts.')
        return contracts

    def set_returns(self):
        returns = []
        for contract in self._contracts:
            contract_returns = contract.get_returns()
            returns.append(contract_returns)
            print(f'Added {contract.get_symbol()} to returns.')
        return returns

# Usage of the Portfolio class
base_path = r'C:\Users\kbott\OneDrive\Desktop\AlgoData\OutputFile\Contract_Data'
list_of_symbols = []

for file_name in os.listdir(base_path):
    if file_name.endswith('_Data.csv'):  # This ensures only the relevant files are considered
        symbol = file_name.replace('&', '').replace('_Data.csv', '')
        list_of_symbols.append(symbol)

# Instantiate Portfolio with equal weights by default
test_port = Portfolio(list_of_symbols)
print(test_port.get_returns())
