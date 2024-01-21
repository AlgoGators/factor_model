from factor import Factor
from portfolio import Portfolio
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import numpy as np
import os

# Set the base path for data files
base_path = r'C:\Users\kbott\OneDrive\Desktop\AlgoData\OutputFile\Contract_Data'
list_of_symbols = []

# Load the symbols
for file_name in os.listdir(base_path):
    if file_name.endswith('_Data.csv'):
        symbol = file_name.replace('&', '').replace('_Data.csv', '')
        list_of_symbols.append(symbol)

# Initialize Portfolio and Factor objects
portfolio = Portfolio(list_of_symbols)
portfolio_returns = portfolio.get_returns()

vix_index = Factor('^VIX', 'Volatility Risk', portfolio_returns.index[0], portfolio_returns.index[-1])
vix_returns = vix_index.get_returns()

# Joining portfolio and VIX returns
combined_data = portfolio_returns.join(vix_returns, how='inner', lsuffix='_portfolio', rsuffix='_vix')

pd.set_option('display.max_rows', None)

output_file_path = os.path.join(r'C:\Users\kbott\OneDrive\Desktop\AlgoData\OutputFile', 'combined_data.csv')
combined_data.to_csv(output_file_path, index=True)
