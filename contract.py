import pandas as pd
from sqlalchemy import create_engine
import urllib
from factor import Factor


class Contract:
    def __init__(self, symbol):
        self._symbol = symbol
        self._closing_prices = self.set_closing_prices()
        self._returns = self.set_returns()

    def set_closing_prices(self) -> pd.DataFrame:
        # Server and database information - *update driver as needed*
        driver = 'ODBC Driver 18 for SQL Server'
        server = 'algo.database.windows.net'
        username = 'dbmaster'
        password = 'Password1'

        # *Change database to NG_Carver_Data_Carry as needed*
        database = 'NG_Carver_Data'

        # Connection string for SQL Server Authentication - do not change
        params = urllib.parse.quote_plus(
            fr'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')
        engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)

        # Retrieve a list of all table names in the database - do not change
        table_names_query = "SELECT table_name FROM information_schema.tables WHERE table_type = 'BASE TABLE' AND table_catalog='" + database + "'"
        table_names = pd.read_sql(table_names_query, engine)['table_name'].tolist()

        contract_df = pd.DataFrame()

        # Loop through all table names, pulling data from each one
        for table_name in table_names:
            if table_name == f'{self._symbol}_Data':
                table_query = f"SELECT * FROM [{table_name}]"
                contract_df = pd.read_sql(table_query, engine)
                contract_df['Date'] = pd.to_datetime(contract_df['Date'])
                contract_df.set_index('Date', inplace=True)
                return contract_df
        else:
            # Return an empty DataFrame if no data was found
            return pd.DataFrame()

    def get_data(self):
        return self._returns

    def get_symbol(self):
        return self._symbol

    def set_returns(self):
        self._closing_prices['Close'] = pd.to_numeric(self._closing_prices['Close'], errors='coerce')

        if not self._closing_prices.empty:
            # Calculate daily returns using pct_change()
            returns = self._closing_prices['Close'].pct_change()

            # Create a new DataFrame for returns
            returns_df = pd.DataFrame(index=self._closing_prices.index)
            returns_df['Return'] = returns
            returns_df['1 + Return'] = returns + 1

            # Return the _returns attribute
            return returns_df.dropna()
        else:
            print("DataFrame is empty.")
            return pd.DataFrame()

    def get_first_date(self):
        return self._closing_prices.index[0]

    def get_returns(self):
        return self._returns


test = Contract('ES')

factor = Factor('^VIX', 'Volatility Risk', test.get_first_date())
print(factor.get_returns())
print(test.get_returns())
