from factor import Factor
import pandas as pd
from contract import Contract
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np

contract_data = Contract('ES').get_data()
vix_index = Factor('^VIX', 'Volatility Risk', contract_data.index[0]).get_closing_prices()

combined_data = contract_data.join(vix_index, how='inner', lsuffix='_contract', rsuffix='_vix')
combined_data.dropna(inplace=True)

X = combined_data[['Close_vix']]
Y = combined_data[['Close_contract']]

reg = LinearRegression()
reg.fit(X, Y)
predictions = reg.predict(X)

plt.scatter(X, Y, color='blue', label='Actual data')
plt.plot(X, predictions, color='red', linewidth=2, label='Regression line')

slope = round(reg.coef_[0][0], 3)
intercept = round(reg.intercept_[0], 3)

equation = f'y = {slope}x + {intercept}'

plt.text(x=plt.gca().get_xlim()[1]/2, y=plt.gca().get_ylim()[1]*0.95, s=equation, color='red', fontsize=12, ha='center')

plt.title('Linear Regression between VIX and ES Contract')
plt.xlabel('VIX Index Closing Prices')
plt.ylabel('ES Contract Closing Prices')

plt.legend()
plt.show()

"""
create classes for portfolio and contract and factor
- each contract should have dataframe with all its data and a name for the symbol
- portfolio will be made up these contracts, need to figure out how to populate the portfolio (as in what contracts do
  we hold and in what quantity)
    - for now will just leave as holding one of each contract until can figure out a better method
    
use returns not prices for closing
- on a contract level object, it will have the full dataframe from SQL server (as in date, name, OHLC, etc not returns)
- need to somehow pull out the data for returns which will have dates as index and a single columns for returns 
- once we have returns on an individual contract basis, we can geometrically link all the returns to get a total return
  for the portfolio for regressions

"""



