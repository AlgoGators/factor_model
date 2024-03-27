import pandas as pd
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler

from contract_portfolio import ContractPortfolio
from factor_portfolio import FactorPortfolio, factor_symbols
import portfolio_utils as utils


def main():
    # Initialize Portfolio objects
    contract_portfolio = ContractPortfolio()
    portfolio_returns = contract_portfolio.get_returns()

    percentile_95 = portfolio_returns['Portfolio Return'].quantile(0.95)
    percentile_5 = portfolio_returns['Portfolio Return'].quantile(0.05)
    portfolio_returns = portfolio_returns[(portfolio_returns['Portfolio Return'] < percentile_95) &
                                          (portfolio_returns['Portfolio Return'] > percentile_5)]

    # Get returns from the portfolios
    factor_portfolio = FactorPortfolio(portfolio_returns.index[0], portfolio_returns.index[-1])
    factor_returns = factor_portfolio.get_returns()

    # Prepare and clean data
    combined_returns = utils.prepare_data(portfolio_returns, factor_returns)

    # Define independent variable (features) and dependent variable
    X = combined_returns[[factor_name for factor_name in factor_symbols.values()]]
    Y = combined_returns['Portfolio Return']

    # Perform grid search to find optimal alpha for Lasso and ElasticNet
    lasso_params, elasticnet_params = utils.perform_grid_search(X, Y)

    # Perform different regressions using the optimal alphas
    models = utils.perform_different_regressions(X, Y, lasso_params['alpha'], elasticnet_params['alpha'])

    # Plot results for each regression model
    utils.plot_all_regression_results(X, Y, models)


if __name__ == "__main__":
    main()
