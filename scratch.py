import os
import glob
import pandas as pd
import openpyxl


base_path = r"C:\Users\kbott\OneDrive\Desktop\AlgoData\LinearRegression (002).xlsx"
df = pd.read_excel(base_path)

print(df)

factor_symbol_dict = {}

for ticker, factor in zip(df['Ticker'], df['Factors']):
    factor_symbol_dict[ticker] = factor

# print all the values in the column 'Norgate Sym'

