import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, Lasso, Ridge, ElasticNet
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler


def prepare_data(portfolio_returns, factor_returns):
    """Join portfolio and factor returns and clean data."""
    combined = portfolio_returns.join(factor_returns, how='inner', lsuffix='_portfolio', rsuffix='_factor')

    # Check for NaN values
    nan_rows = combined[combined.isnull().any(axis=1)]
    if not nan_rows.empty:
        print(f'Rows with NaN values: {nan_rows}')
        combined.dropna(inplace=True)

    # Check for infinite values
    infinite_rows = combined[np.isinf(combined).any(axis=1)]
    if not infinite_rows.empty:
        print(f'Rows with infinite values: {infinite_rows}')
        combined.replace([np.inf, -np.inf], np.nan, inplace=True)
        combined.dropna(inplace=True)

    return combined


def perform_grid_search(X, Y):
    """Perform grid search to find optimal alpha for Lasso and ElasticNet"""
    lasso = Lasso(max_iter=10000, random_state=42)
    elasticnet = ElasticNet(max_iter=10000, random_state=42)
    parameters = {'alpha': [1e-4, 1e-3, 1e-2, 1e-1, 1, 10, 100]}

    lasso_regressor = GridSearchCV(lasso, parameters, scoring='r2', cv=5)
    elasticnet_regressor = GridSearchCV(elasticnet, parameters, scoring='r2', cv=5)

    lasso_regressor.fit(X, Y)
    elasticnet_regressor.fit(X, Y)

    return lasso_regressor.best_params_, elasticnet_regressor.best_params_


def perform_different_regressions(X, Y, lasso_alpha, elasticnet_alpha):
    """Perform Linear, Lasso, Ridge, and ElasticNet regression and return the models."""
    models = {
        'Linear': LinearRegression(),
        'Lasso': Lasso(alpha=lasso_alpha, max_iter=10000),
        'Ridge': Ridge(alpha=1.0),  # Default alpha=1.0, may require tuning
        'ElasticNet': ElasticNet(alpha=elasticnet_alpha, l1_ratio=0.7, max_iter=10000)  # l1_ratio may require tuning
    }
    for name, model in models.items():
        model.fit(X, Y)
        models[name] = model  # Update with the fitted model
    return models


def plot_regression_results(ax, X, Y, model, model_name):
    """Plot the results of the regression on a given axes."""
    x_values = np.array([X.min(), X.max()])
    y_values = model.coef_[0] * x_values + model.intercept_
    ax.scatter(X, Y, color='blue')
    ax.plot(x_values, y_values, color='red')
    ax.set_title(f'{model_name} Regression')
    ax.set_xlabel('Factor Returns')
    ax.set_ylabel('Portfolio Returns')

    # Calculate and display the equation and adjusted R-squared
    adjusted_r_squared = calculate_adjusted_r_squared(Y, model.predict(X.reshape(-1, 1)), X)
    equation = f'y = {model.coef_[0]: .4f}x + {model.intercept_: .4f}'
    ax.text(0.95, 0.05, f'{equation}\nAdj. R-squared: {adjusted_r_squared: .4f}',
            ha='right', va='bottom', transform=ax.transAxes, fontsize=9, color='black')


def plot_all_regression_results(X, Y, models):
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))  # Create a 2x2 grid of subplots
    axs = axs.flatten()  # Flatten the 2D array of axes for easy iteration

    for ax, (name, model) in zip(axs, models.items()):
        plot_regression_results(ax, X, Y, model, name)

    plt.tight_layout()  # Adjust subplots to fit into the figure area
    plt.show()


def calculate_adjusted_r_squared(Y, Y_pred, X):
    """Calculate R-squared and adjusted R-squared."""
    r_squared = r2_score(Y, Y_pred)
    n = len(Y)
    # If X is a DataFrame, get the number of columns; if Series or ndarray, treat as single predictor
    p = X.shape[1] if isinstance(X, pd.DataFrame) else 1
    adjusted_r_squared = 1 - ((1 - r_squared) * (n - 1) / (n - p - 1))
    return adjusted_r_squared
