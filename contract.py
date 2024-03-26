import pandas as pd
import psycopg2
import toml
from typing import Dict, Any
import numpy as np
from sqlalchemy import create_engine
import urllib
from factor import Factor
from percent_change import get_df_percent_change
from psycopg2.extensions import connection as PGConnection
from psycopg2 import sql

config_data: Dict[str, Any] = toml.load(r'config.toml')

# Setup PostgreSQL database parameters from the configuration data for later connection.
DB_PARAMS: Dict[str, Any] = {
    'dbname': config_data['database']['db_trend'],
    'user': config_data['database']['user'],
    'password': config_data['database']['password'],
    'host': config_data['server']['ip'],
    'port': config_data['database']['port']
}


def fetch_symbol_dict() -> Dict[str, str]:
    # Define the path to the CSV file that contains mapping of symbols to datasets.
    path_to_csv: str = r'contracts.csv'
    # Load the CSV file into a pandas DataFrame.
    df: pd.DataFrame = pd.read_csv(path_to_csv)
    # Convert the DataFrame into a dictionary with 'Data Symbol' as keys and 'Data Set' as values for easy lookup.
    symbol_dict: Dict[str, str] = df.set_index('Data Symbol')['Data Set'].to_dict()

    return symbol_dict


def get_connection() -> PGConnection:
    # Establish and return a connection object to the PostgreSQL database using psycopg2.
    conn: PGConnection = psycopg2.connect(**DB_PARAMS)

    return conn


def get_data_from_db(symbol: str) -> pd.DataFrame:
    # Get a database connection.
    conn: PGConnection = get_connection()

    # Open a new database cursor for executing SQL commands.
    with conn.cursor() as cur:
        create_table_query: str = f"""
        SELECT * FROM "{symbol}_data";
        """
        # Execute the SQL query to create a new table for the symbol.
        cur.execute(create_table_query)
        # Fetch all the rows from the result of the executed query.
        rows = cur.fetchall()
        # Convert the rows into a pandas DataFrame.
        df = pd.DataFrame(rows)
        # Close the cursor.
        cur.close()
        # Close the connection.
        conn.close()

    return df


class Contract:
    def __init__(self, symbol):
        self._symbol = symbol
        self._price_data = self.set_price_data()
        self._returns = self.set_returns()

    def set_price_data(self) -> pd.DataFrame:
        contract_df = get_data_from_db(self._symbol)

        # Check for NaN values
        nan_rows = contract_df[contract_df.isnull().any(axis=1)]
        if not nan_rows.empty:
            print(f'Symbol {self._symbol} has these rows with NaN values: {nan_rows}')
            contract_df.dropna(inplace=True)

        return contract_df

    def get_data(self):
        return self._price_data

    def get_symbol(self):
        return self._symbol

    def set_returns(self):
        self._price_data[6] = pd.to_numeric(self._price_data[6], errors='coerce')

        if not self._price_data.empty:
            # Calculate daily returns using new function
            returns = get_df_percent_change(self._price_data[[6, 12]]).dropna()
            returns.set_index(self._price_data[0][:len(returns)], inplace=True)

            # Create a new DataFrame for returns
            returns_df = pd.DataFrame(index=returns.index)
            returns_df['Return'] = returns[['Percent Change']]
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
