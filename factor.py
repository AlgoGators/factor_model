import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta


class Factor:

    def __init__(self, ticker, factor, start_date):
        self._ticker = ticker
        self._factor = factor
        self._start_date = start_date
        self._price_data = self.set_price_data()
        self._returns = self.set_returns()


    def set_price_data(self) -> pd.DataFrame:
        end_date = datetime.today()
        data = yf.download(self._ticker, start=self._start_date, end=end_date)
        return data

    def set_returns(self):
        self._price_data['Close'] = pd.to_numeric(self._price_data['Close'], errors='coerce')

        if not self._price_data.empty:
            # Calculate daily returns using pct_change()
            returns = self._price_data['Close'].pct_change()

            # Create a new DataFrame for returns
            returns_df = pd.DataFrame(index=self._price_data.index)
            returns_df['Return'] = returns
            returns_df['1 + Return'] = returns + 1

            # Return the _returns attribute
            return returns_df.dropna()
        else:
            print("DataFrame is empty.")
            return pd.DataFrame()


    def get_closing_prices(self):
        return self._price_data['Close']

    def get_returns(self):
        return self._returns


