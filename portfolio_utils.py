import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, Lasso, Ridge, ElasticNet
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV


def linear_regression(X, Y):
    """
    Perform Linear regression and return the model.
    :param X: independent variable
    :param Y: dependent variable

    :return: Linear regression model
    """
    model = LinearRegression()
    model.fit(X, Y)
    return model


def lasso_regression(X, Y):
    """
    Perform Lasso regression and return the model.
    :param X: independent variable
    :param Y: dependent variable

    :return: Lasso regression model
    """
    alpha = find_optimal_alpha(Lasso, X, Y)
    model = Lasso(alpha=alpha)
    model.fit(X, Y)
    return model


def ridge_regression(X, Y):
    """
    Perform Ridge regression and return the model.
    :param X: independent variable
    :param Y: dependent variable

    :return: Ridge regression model
    """
    alpha = find_optimal_alpha(Ridge, X, Y)
    model = Ridge(alpha=alpha)
    model.fit(X, Y)
    return model


def elasticnet_regression(X, Y):
    """
    Perform ElasticNet regression and return the model.
    :param X: independent variable
    :param Y: dependent variable

    :return: ElasticNet regression model"""
    alpha = find_optimal_alpha(ElasticNet, X, Y)
    model = ElasticNet(alpha=alpha)
    model.fit(X, Y)
    return model


def find_optimal_alpha(model_type, X, Y):
    """
    Find the optimal alpha for the given model type using GridSearchCV.
    :param model_type: type of model to use
    :param X: independent variable
    :param Y: dependent variable

    :return: optimal alpha value
    """
    alphas = np.logspace(-4, 4, 100)
    model = model_type()
    grid = GridSearchCV(estimator=model, param_grid=dict(alpha=alphas), cv=5)
    grid.fit(X, Y)
    print(f'Best alpha for {model_type.__name__}: {grid.best_estimator_.alpha}')
    return grid.best_estimator_.alpha


def prepare_data(portfolio_returns, factor_returns):
    """
    Prepare the data by aligning the dates of portfolio and factor returns.
    :param portfolio_returns: DataFrame of portfolio returns
    :param factor_returns: DataFrame of factor returns

    :return: Aligned DataFrames of portfolio and factor returns
    """
    # Align portfolio returns with factor returns by index
    common_index = portfolio_returns.index.intersection(factor_returns.index)
    portfolio_aligned = portfolio_returns.loc[common_index]
    factor_aligned = factor_returns.loc[common_index]
    return portfolio_aligned, factor_aligned


def run_regressions(X, Y):
    """
    Run different types of regressions and return their intercepts and coefficients.
    :param X: independent variable
    :param Y: dependent variable

    :return: dictionary of regression results
    """
    results = {}
    models = {
        'Linear': linear_regression,
        'Ridge': ridge_regression,
        'Lasso': lasso_regression,
        'ElasticNet': elasticnet_regression
    }
    for name, model_func in models.items():
        model = model_func(X, Y)
        results[f'{name}_Intercept'] = model.intercept_
        results[f'{name}_Coeff'] = model.coef_[0] if hasattr(model.coef_, '__len__') else model.coef_
    return results


def get_regression_results(portfolio_returns, factor_returns, info_type='intercepts'):
    """ Calculate regression intercepts or coefficients for each asset-factor pair.
    :param portfolio_returns: DataFrame of portfolio returns
    :param factor_returns: DataFrame of factor returns
    :param info_type: type of information to return (intercepts or coefficients)

    :return: DataFrame of regression results
    """
    portfolio_aligned, factor_aligned = prepare_data(portfolio_returns, factor_returns)
    results_dict = {}

    # Define dictionary keys based on the required information type
    if info_type == 'intercepts':
        keys = ['Linear_Intercept', 'Ridge_Intercept', 'Lasso_Intercept', 'ElasticNet_Intercept']
    else:
        keys = ['Linear_Coeff', 'Ridge_Coeff', 'Lasso_Coeff', 'ElasticNet_Coeff']

    for key in keys:
        results_dict[key] = []

    # Loop over assets and factors
    for asset in portfolio_aligned.columns:
        for factor in factor_aligned.columns:
            Y = portfolio_aligned[asset]
            X = factor_aligned[[factor]]
            regression_results = run_regressions(X, Y)

            # Append results to the dictionary
            for key in keys:
                results_dict[key].append(regression_results[key])

    # Create DataFrame and set appropriate index
    results_df = pd.DataFrame(results_dict)
    results_df.index = [f'{asset}: {factor}' for asset in portfolio_aligned.columns for factor in
                        factor_aligned.columns]

    return results_df


def get_intercepts_df(portfolio_returns, factor_returns):
    """
    Get alpha intercepts from each regression model.
    :param portfolio_returns: DataFrame of portfolio returns
    :param factor_returns: DataFrame of factor returns

    :return: DataFrame of alpha intercepts
    """
    return get_regression_results(portfolio_returns, factor_returns, info_type='intercepts')


def get_coefficients_df(portfolio_returns, factor_returns):
    """
    Get beta coefficients from each regression model.
    :param portfolio_returns: DataFrame of portfolio returns
    :param factor_returns: DataFrame of factor returns

    :return: DataFrame of beta coefficients
    """
    return get_regression_results(portfolio_returns, factor_returns, info_type='coefficients')


def plot_regression_results(ax, X, Y, model, model_name):
    """
    Plot the results of the regression for models with multiple independent variables.
    :param ax: Matplotlib axis object
    :param X: independent variable
    :param Y: dependent variable
    :param model: regression model
    :param model_name: name of the model
    """
    # Predicted vs. actual values
    Y_pred = model.predict(X)
    ax.scatter(Y, Y_pred, color='blue')  # Actual vs. Predicted scatter plot
    ax.plot([X.min(), X.max()], [Y.min(), Y.max()], 'k--', lw=4, color='red')  # Diagonal line for reference
    ax.set_title(f'{model_name} Regression')
    ax.set_xlabel('Actual Portfolio Returns')
    ax.set_ylabel('Predicted Portfolio Returns')

    # Calculate and display the adjusted R-squared
    adjusted_r_squared = calculate_adjusted_r_squared(Y, Y_pred, X.shape[1])  # Update the calculation if necessary
    ax.text(0.05, 0.95, f'Adj. R-squared: {adjusted_r_squared: .4f}',
            ha='left', va='top', transform=ax.transAxes, fontsize=9, color='black')

    # Display model coefficients in tabular format
    coefs_table = '\n'.join([f'$\\beta_{{{i + 1}}}$: {coef:.4f}' for i, coef in enumerate(model.coef_)])
    props = dict(boxstyle='round', facecolor='white', alpha=0.5)
    ax.text(0.05, 0.90, coefs_table, transform=ax.transAxes, fontsize=9,
            verticalalignment='top', bbox=props)

    # Optionally, adjust the limits if necessary to prevent overlap
    ax.set_xlim(left=min(Y.min(), Y_pred.min()), right=max(Y.max(), Y_pred.max()))
    ax.set_ylim(bottom=min(Y.min(), Y_pred.min()), top=max(Y.max(), Y_pred.max()))


def plot_all_regression_results(X, Y, models):
    """
    Plot the results of the regression for multiple models.
    :param X: independent variable
    :param Y: dependent variable
    :param models: dictionary of regression models
    """
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))  # Create a 2x2 grid of subplots
    axs = axs.flatten()  # Flatten the 2D array of axes for easy iteration

    for ax, (name, model) in zip(axs, models.items()):
        plot_regression_results(ax, X, Y, model, name)

    plt.tight_layout()  # Adjust subplots to fit into the figure area
    plt.show()


def calculate_adjusted_r_squared(Y, Y_pred, X):
    """
    Calculate R-squared and adjusted R-squared.
    :param Y: dependent variable
    :param Y_pred: predicted dependent variable
    :param X: independent variable

    :return: adjusted R-squared value
    """
    r_squared = r2_score(Y, Y_pred)
    n = len(Y)
    # If X is a DataFrame, get the number of columns; if Series or ndarray, treat as single predictor
    p = X.shape[1] if isinstance(X, pd.DataFrame) else 1
    adjusted_r_squared = 1 - ((1 - r_squared) * (n - 1) / (n - p - 1))
    return adjusted_r_squared
