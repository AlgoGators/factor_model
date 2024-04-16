import pandas as pd
import numpy as np
from portfolio import Portfolio
from contract import Contract


class ContractPortfolio(Portfolio):
    def __init__(self, contract_symbols=None, weighting=None, start_date=None, end_date=None):
        super().__init__(contract_symbols, weighting, start_date, end_date)

    def initialize_components(self):
        """
        Initialize Contract objects for each symbol in the portfolio.

        :return: A list of Contract objects
        """
        contracts = []
        index = 0
        for symbol in self._symbol_list:
            # Retrieve the number of contracts held for the symbol; default is 1
            num_contracts_held = self._weighting.get(symbol, 1)
            # Create and add Contract objects to the list
            index += 1
            for _ in range(num_contracts_held):
                contracts.append(Contract(symbol))
                print(f"Contract {index} / {len(self._symbol_list)} ({symbol}) added to the portfolio.")
            if index == 5:
                # pass
                break

        print(f'Contract Portfolio initialized with {len(contracts)} contracts: '
              f'start date = {self._start_date} \t end date = {self._end_date}')

        return contracts

    def aggregate_returns(self):
        """
        Aggregate returns from each contract in the portfolio.
        This method assumes that each Contract object has a 'get_returns' method
        that returns a DataFrame with a 'Return' column.

        :return: A pandas DataFrame containing the aggregated returns
        """
        # List to hold 'Return' columns from each contract's DataFrame
        returns_columns = []

        for contract in self._components:
            contract_returns_df = contract.get_returns()
            contract_returns_df.replace([np.inf, -np.inf], np.nan, inplace=True)
            contract_returns_df.dropna(inplace=True)

            # Convert index to Datetime object with a standard format
            contract_returns_df.index = pd.to_datetime(contract_returns_df.index)

            if 'Return' in contract_returns_df.columns:
                returns_columns.append(contract_returns_df[['Return']])
            else:
                raise ValueError(f"Contract {contract.get_symbol()} DataFrame missing 'Return' column.")

        # Concatenate all 'Return' columns along the column axis using outer join
        returns_df = pd.concat(returns_columns, axis=1, join='outer')
        returns_df.dropna(inplace=True)

        # Add contract symbol name as name of column
        returns_df.columns = [contract.get_symbol() for contract in self._components]

        return returns_df
