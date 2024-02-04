import pandas as pd
from factor_model.portfolio import Portfolio  # Assuming the abstract base class is in portfolio.py
from factor import Factor  # Assuming the Factor class is defined in factor.py


factor_symbols = ['SPY', '^VIX', '^TNX', 'SWRSX', 'CRMZ', '^SPGSCI', 'XAE=F', '^DJGSP', 'JJATF', 'VWO', 'VEA', '^FTW5000']


class FactorPortfolio(Portfolio):

    def __init__(self, start_date, end_date, holdings=None):
        self._start_date = start_date
        self._end_date = end_date

        print(f"FactorPortfolio initialized with start date: {start_date} and end date: {end_date}")
        super().__init__(factor_symbols, holdings)



    def initialize_components(self):
        """
        Initialize Factor objects for each symbol in the portfolio.

        :return: A list of Factor objects
        """
        factors = [Factor(symbol, self._start_date, self._end_date) for symbol in self._symbol_list]
        return factors


    def aggregate_returns(self):
        """
        Aggregate returns from each factor in the portfolio.
        This method assumes that each Factor object has a 'get_returns' method
        that returns a DataFrame with a 'Return' column.

        :return: A pandas DataFrame containing the aggregated returns
        """
        # List to hold '1 + Return' columns from each factor's DataFrame
        one_plus_return_cols = []

        for factor in self._components:
            factor_returns_df = factor.get_returns()
            # Verify the '1 + Return' column exists
            if '1 + Return' in factor_returns_df.columns:
                # We could weight the returns by factor_weight if applicable
                one_plus_return_cols.append(factor_returns_df['1 + Return'])
            else:
                print(f"Factor {factor.get_ticker()} DataFrame missing '1 + Return' column.")

        # Concatenate all '1 + Return' columns along the column axis using inner join
        all_returns = pd.concat(one_plus_return_cols, axis=1, join='inner')

        # Calculate the product of '1 + Return' across all factors (row-wise)
        portfolio_1_plus_return = all_returns.prod(axis=1, skipna=False)

        # Create portfolio DataFrame
        portfolio_df = pd.DataFrame(index=all_returns.index)
        portfolio_df['1 + Return'] = portfolio_1_plus_return
        portfolio_df['Return'] = portfolio_1_plus_return - 1

        return portfolio_df.dropna()

# Example usage:
# Assuming list_of_symbols is a list of factor tickers
# factor_portfolio = FactorPortfolio(list_of_symbols)
# print(factor_portfolio.get_returns())
