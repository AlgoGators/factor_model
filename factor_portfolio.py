import pandas as pd
from portfolio import Portfolio
from factor import Factor


class FactorPortfolio(Portfolio):
    def __init__(self, factor_symbols=None, start_date=None, end_date=None, weighting=None):
        super().__init__(factor_symbols, weighting, start_date, end_date)

    def initialize_components(self):
        """
        Initialize Factor objects for each symbol in the portfolio.

        :return: A list of Factor objects
        """
        factors = [Factor(symbol, factor_name, self._start_date, self._end_date) for symbol, factor_name in
                   self._symbol_list.items()]

        print(f'Factor Portfolio initialized with {len(factors)} factors: ' 
              f'start date = {self._start_date} \t end date = {self._end_date}')

        return factors

    def aggregate_returns(self):
        """
        Aggregate returns from each factor in the portfolio.
        This method assumes that each Factor object has a 'get_returns' method
        that returns a DataFrame with a 'Return' column.

        :return: A pandas DataFrame containing the aggregated returns
        """
        # List to hold 'Return' columns from each factor's DataFrame
        return_cols = {}

        for factor in self._components:
            factor_returns_df = factor.get_returns()

            # Add 'Return' column to return_cols dictionary
            if 'Return' in factor_returns_df.columns:
                return_cols[factor.get_factor_name()] = factor_returns_df['Return']
            else:
                print(f"Factor {factor.get_factor_name()} DataFrame missing 'Return' column.")

        # Concatenate all 'Return' columns along the column axis using inner join
        returns_df = pd.concat(return_cols, axis=1, join='inner')
        returns_df.dropna(inplace=True)

        return returns_df
