import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import urllib
from factor import Factor
from percent_change import get_df_percent_change


class Contract:
    def __init__(self, symbol):
        self._symbol = symbol
        self._price_data = self.set_price_data()
        self._returns = self.set_returns()

    def set_price_data(self) -> pd.DataFrame:
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

                # Check for NaN values
                nan_rows = contract_df[contract_df.isnull().any(axis=1)]
                if not nan_rows.empty:
                    print(f'Symbol {self._symbol} has these rows with NaN values: {nan_rows}')
                    contract_df.dropna(inplace=True)

                # Ensure all data is numeric before checking for infinite values
                contract_df = contract_df.apply(pd.to_numeric, errors='coerce')

                # Now it's safe to check for infinite values
                infinite_rows = contract_df[np.isinf(contract_df).any(axis=1)]

                if not infinite_rows.empty:
                    print(f'Rows with infinite values: {infinite_rows}')
                    contract_df.replace([np.inf, -np.inf], np.nan, inplace=True)
                    contract_df.dropna(inplace=True)
                return contract_df
        else:
            # Return an empty DataFrame if no data was found
            return pd.DataFrame()

    def get_data(self):
        return self._price_data

    def get_symbol(self):
        return self._symbol

    def set_returns(self):
        self._price_data['Unadj_Close'] = pd.to_numeric(self._price_data['Unadj_Close'], errors='coerce')

        if not self._price_data.empty:
            # Calculate daily returns using new function
            returns = get_df_percent_change(self._price_data[['Unadj_Close', 'Delivery Month']])

            # Create a new DataFrame for returns
            returns_df = pd.DataFrame(index=self._price_data.index)
            returns_df['Return'] = returns
            returns_df['1 + Return'] = returns + 1

            # Return the _returns attribute
            return returns_df.dropna()
        else:
            print(f"{self._symbol} DataFrame is empty.")
            return pd.DataFrame()

    def get_first_date(self):
        print(self._price_data.index[0])
        return self._price_data.index[0]

    def get_last_date(self):
        print(self._price_data.index[-1])
        return self._price_data.index[-1]

    def get_returns(self):
        return self._returns

# factor = Factor('^VIX', 'Volatility Risk', test.get_first_date(), test.get_last_date())
# print(factor.get_returns())
# pd.set_option('display.max_columns', None)
# print(test.get_returns())
