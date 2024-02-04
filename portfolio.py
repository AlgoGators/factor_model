from abc import ABC, abstractmethod
import pandas as pd


class Portfolio(ABC):
    def __init__(self, symbol_list, holdings=None):
        """
        Initialize a Portfolio with a list of symbols and optional holdings.

        :param symbol_list: List of symbol identifiers for the portfolio components
        :param holdings: Dictionary mapping symbols to the number of units held
        """
        self._symbol_list = symbol_list
        self._holdings = holdings if holdings is not None else {symbol: 1 for symbol in symbol_list}
        self._components = self.initialize_components()
        self._returns = self.aggregate_returns()

    @abstractmethod
    def initialize_components(self):
        """
        Initialize the components of the portfolio (contracts or factors).
        This method should be implemented by subclasses to create the specific
        components relevant to the type of portfolio.

        :return: A list of initialized portfolio components
        """
        pass

    @abstractmethod
    def aggregate_returns(self):
        """
        Aggregate the returns from the portfolio components.
        This method should be implemented by subclasses to calculate the
        portfolio's returns based on the individual component returns.

        :return: A pandas DataFrame containing the aggregated returns
        """
        pass

    def get_returns(self):
        """
        Public method to access the aggregated returns of the portfolio.

        :return: A pandas DataFrame containing the portfolio's returns
        """
        return self._returns
