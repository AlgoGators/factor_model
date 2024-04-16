from abc import ABC, abstractmethod
from datetime import datetime, timedelta


class Portfolio(ABC):
    def __init__(self, symbol_list, weighting=None, start_date=None, end_date=None):
        """
        Initialize a Portfolio with a list of symbols and optional holdings.

        :param symbol_list: List of symbol identifiers for the portfolio components
        :param weighting: Dictionary mapping symbols to the number of units held
        :param start_date: The start date for the portfolio's returns
        :param end_date: The end date for the portfolio's returns
        """
        self._symbol_list = symbol_list
        self._weighting = weighting if weighting is not None else {symbol: 1 for symbol in symbol_list}

        if start_date is None:
            start_date = datetime.today() - timedelta(days=10 * 365)
        if end_date is None:
            end_date = datetime.today()

        self._start_date = start_date
        self._end_date = end_date

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
