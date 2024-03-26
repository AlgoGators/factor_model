import pandas as pd
from portfolio import Portfolio
from factor import Factor

factor_symbols = {'^VIX': 'Volatility Risk',
                  '^TNX': 'Interest Rate Risk',
                  'SWRSX': 'Inflation Risk',
                  'CRMZ': 'Credit Risk',
                  'SPY': 'Equity Market Risk',
                  'DX-Y.NYB': 'Currency Risk',
                  '^SPGSCI': 'Commodity Price Risk',
                  'XAE=F': 'Energy Price Risk',
                  '^DJGSP': 'Metals Price Risk',
                  'JJATF': 'Agricultural Price Risk',
                  'VWO': 'Emerging Market Risk',
                  'VEA': 'Developed Market Risk',
                  '^FTW5000': 'Systematic Risk'}


class FactorPortfolio(Portfolio):

    def __init__(self, start_date, end_date, holdings=None):
        self._start_date = start_date
        self._end_date = end_date

        print(f"FactorPortfolio initialized with start date: {start_date} and end date: {end_date}")
        super().__init__(factor_symbols.keys(), holdings)

    def initialize_components(self):
        """
        Initialize Factor objects for each symbol in the portfolio.

        :return: A list of Factor objects
        """
        factors = [Factor(symbol, factor_name, self._start_date, self._end_date) for symbol, factor_name in
                   factor_symbols.items()]
        return factors

    def aggregate_returns(self):
        """
        Aggregate returns from each factor in the portfolio.
        This method assumes that each Factor object has a 'get_returns' method
        that returns a DataFrame with a 'Return' column.

        :return: A pandas DataFrame containing the aggregated returns
        """
        # List to hold '1 + Return' columns from each factor's DataFrame
        one_plus_return_cols = {}

        for factor in self._components:
            factor_returns_df = factor.get_returns()
            # Verify the '1 + Return' column exists
            if 'Return' in factor_returns_df.columns:
                # We could weight the returns by factor_weight if applicable
                one_plus_return_cols[factor.get_factor_name()] = factor_returns_df['Return']
            else:
                print(f"Factor {factor.get_factor_name()} DataFrame missing 'Return' column.")

        # Concatenate all '1 + Return' columns along the column axis using inner join
        all_returns = pd.concat(one_plus_return_cols, axis=1, join='inner')

        return all_returns.dropna()


# Example usage:
# Assuming list_of_symbols is a list of factor tickers
# factor_portfolio = FactorPortfolio('2000-1-1', '2023-12-13')
# print(factor_portfolio.get_returns())
