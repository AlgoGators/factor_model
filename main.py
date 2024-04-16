import pandas as pd

from contract_portfolio import ContractPortfolio
from factor_portfolio import FactorPortfolio
import portfolio_utils as utils


def main():
    contract_symbols = ['6A', '6B', '6C', '6E', '6J', '6M', '6N', '6S', 'CT', 'ES', 'FCE', 'FDAX', 'FSMI', 'GC',
                        'GF', 'HE', 'HG', 'KC', 'KE', 'LE', 'LRC', 'LSU', 'NQ', 'PL', 'RB', 'RTY', 'SB', 'SCN',
                        'SI', 'UB', 'VX', 'WBS', 'YM', 'ZC', 'ZL', 'ZM', 'ZN', 'ZR', 'ZS', 'ZW']

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

    # Initialize Portfolio objects
    contract_portfolio = ContractPortfolio(contract_symbols)
    portfolio_returns = contract_portfolio.get_returns()

    # Get returns from the portfolios
    factor_portfolio = FactorPortfolio(factor_symbols)
    factor_returns = factor_portfolio.get_returns()

    # Get alpha intercepts from each regression model
    alphas_df = utils.get_intercepts_df(portfolio_returns, factor_returns)

    # Get beta coefficients from each regression model
    betas_df = utils.get_coefficients_df(portfolio_returns, factor_returns)

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    print(alphas_df)
    print(betas_df)
    exit()

    """
    All of the coefficients here seem to be close to zero. Look into either scaling the data or exploring
    other factors that may be more relevant to the portfolio. Also figure out the best way to use the 
    GridSearchCV function - it's taking too long to find the optimal alpha for each instrument and model combo.
    """

    # Plot results for each regression model
    utils.plot_all_regression_results(X, Y, models)


if __name__ == "__main__":
    main()
