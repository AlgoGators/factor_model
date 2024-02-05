import pandas as pd


def get_percent_change(a: float, b: float) -> float:
    """
    Calculates the percentage change between two numbers. a is the initial value and b is the final value.
    
    Parameters:
    ---
        a: A float representing the initial value
        b: A float representing the final value
    Returns:
    ---
    A float representing the percentage change
    """

    if a == 0:
        return None

    if a > 0:
        return (b - a) / a

    return (b - a) / -a


def get_column_percent_change(
        df: pd.DataFrame,
        column: str = "Unadj_Close") -> pd.DataFrame:
    """
    Calculates the percentage change for adjusted prices. 

    Parameters:
    ---
        df: A pandas DataFrame
        column: A string representing the column with adjusted prices
    
    Returns:
    ---
    A pandas DataFrame with the percentage change
    """
    dates = df.index.tolist()[1:]
    percent_changes = []

    for i in range(1, len(df)):
        percent_changes.append(get_percent_change(df.iloc[i - 1][column], df.iloc[i][column]))

    percent_change_df = pd.DataFrame(percent_changes, columns=["Percent Change"])
    percent_change_df["Date"] = dates
    percent_change_df.set_index("Date", inplace=True)

    return percent_change_df


def get_df_percent_change(
        df: pd.DataFrame,
        unadj_column: str = "Unadj_Close",
        delivery_column: str = "Delivery Month"):
    """
    Calculates the percentage change for unadjusted prices; note this will not look at % change
    between delivery months, but rather the % change within the same delivery month. 
    The missing data points, ~50+ rolls, is not a greater loss than the benefit of having accurate
    true % change (non-adjusted)

    Parameters:
    ---
        df: A pandas DataFrame
        unadj_column: A string representing the column with unadjusted prices
        delivery_column: A string representing the column with delivery month
    
    Returns:
    ---
    A pandas DataFrame with the percentage change
    """

    # creates a set of unique delivery months
    delivery_months: set = set(df[delivery_column].tolist())
    # converts back to list for iterating
    delivery_months: list = list(delivery_months)
    delivery_months.sort()

    percent_returns = pd.DataFrame()

    for delivery_month in delivery_months:
        # creates a dataframe for each delivery month
        df_delivery_month = df[df[delivery_column] == delivery_month]
        delivery_month_returns = get_column_percent_change(df_delivery_month, unadj_column)
        percent_returns = pd.concat([percent_returns, delivery_month_returns])

    return percent_returns
