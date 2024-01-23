from factor import Factor
from portfolio import Portfolio
from portfolio import list_of_symbols
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import numpy as np
import os

# Initialize Portfolio and Factor objects
portfolio = Portfolio(list_of_symbols)
portfolio_returns = portfolio.get_returns()

vix_index = Factor('^VIX', 'Volatility Risk', portfolio_returns.index[0], portfolio_returns.index[-1])
vix_returns = vix_index.get_returns()

# Joining portfolio and VIX returns
combined_data = portfolio_returns.join(vix_returns, how='inner', lsuffix='_portfolio', rsuffix='_vix')

nan_rows = combined_data[combined_data.isnull().any(axis=1)]
if not nan_rows.empty:
    print(f'Rows with NaN values: {nan_rows}')
    combined_data.dropna(inplace=True)

infinite_rows = combined_data[np.isinf(combined_data).any(axis=1)]
if not infinite_rows.empty:
    print(f'Rows with infinite values: {infinite_rows}')
    combined_data.replace([np.inf, -np.inf], np.nan, inplace=True)
    combined_data.dropna(inplace=True)

X = combined_data[['Return_vix']]
Y = combined_data['Return_portfolio']

model = LinearRegression()
model.fit(X, Y)

# using the linear equation y = mx + b
m = model.coef_[0]
b = model.intercept_

plt.scatter(combined_data['Return_vix'], combined_data['Return_portfolio'], color='blue')

x_values = np.array([min(combined_data['Return_vix']), max(combined_data['Return_vix'])])
y_values = m * x_values + b
plt.plot(x_values, y_values, color='red')

plt.xlabel('VIX Returns')
plt.ylabel('Portfolio Returns')
plt.title('Linear Regression between Portfolio and VIX Returns')

equation = f'y = {m: .2f}x + {b: .2f}'
plt.text(0.5, 0.9, equation, ha='center', va='center', transform=plt.gca().transAxes, color='red')

plt.show()
