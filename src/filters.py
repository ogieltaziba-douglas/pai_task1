"""
Filters Module

This module provides functions for filtering public health
vaccination data by various criteria.

Functions:
    filter_by_country: Filter by country/region
    filter_by_date_range: Filter by date range
    filter_by_value_range: Filter by numeric value range
    filter_by_category: Filter by category values
    apply_filters: Apply multiple filters at once
"""

import pandas as pd
from datetime import datetime
from typing import List, Optional


def filter_by_country(
    df: pd.DataFrame, countries: List[str], column: str = "location"
) -> pd.DataFrame:
    """
    Filter DataFrame by country or region.

    Args:
        df: DataFrame to filter.
        countries: List of country names to include.
        column: Column name to filter on (default: 'location').

    Returns:
        Filtered DataFrame containing only specified countries.

    Example:
        >>> filtered = filter_by_country(df, ['United Kingdom', 'Germany'])
        >>> filtered = filter_by_country(df, ['GBR', 'DEU'], column='iso_code')
    """
    if column not in df.columns:
        return df.head(0)  # Return empty DataFrame with same structure

    return df[df[column].isin(countries)].copy()


def filter_by_date_range(
    df: pd.DataFrame,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    date_column: str = "date",
) -> pd.DataFrame:
    """
    Filter DataFrame by date range.

    Args:
        df: DataFrame to filter.
        start_date: Start of date range (inclusive). If None, no lower bound.
        end_date: End of date range (inclusive). If None, no upper bound.
        date_column: Column name containing dates (default: 'date').

    Returns:
        Filtered DataFrame within the date range.

    Example:
        >>> from datetime import datetime
        >>> start = datetime(2021, 1, 1)
        >>> end = datetime(2021, 12, 31)
        >>> filtered = filter_by_date_range(df, start, end)
    """
    if date_column not in df.columns:
        return df.head(0)

    result = df.copy()

    # Ensure date column is datetime
    if not pd.api.types.is_datetime64_any_dtype(result[date_column]):
        result[date_column] = pd.to_datetime(result[date_column])

    if start_date is not None:
        result = result[result[date_column] >= start_date]

    if end_date is not None:
        result = result[result[date_column] <= end_date]

    return result


def filter_by_value_range(
    df: pd.DataFrame,
    column: str,
    min_val: Optional[float] = None,
    max_val: Optional[float] = None,
) -> pd.DataFrame:
    """
    Filter DataFrame by numeric value range.

    Args:
        df: DataFrame to filter.
        column: Column name to filter on.
        min_val: Minimum value (inclusive). If None, no lower bound.
        max_val: Maximum value (inclusive). If None, no upper bound.

    Returns:
        Filtered DataFrame with values within the range.

    Example:
        >>> filtered = filter_by_value_range(df, 'total_vaccinations',
        ...                                   min_val=1000000, max_val=5000000)
    """
    if column not in df.columns:
        return df.head(0)

    result = df.copy()

    if min_val is not None:
        result = result[result[column] >= min_val]

    if max_val is not None:
        result = result[result[column] <= max_val]

    return result


def filter_by_category(
    df: pd.DataFrame, column: str, values: List[str]
) -> pd.DataFrame:
    """
    Filter DataFrame by category values.

    Args:
        df: DataFrame to filter.
        column: Column name to filter on.
        values: List of category values to include.

    Returns:
        Filtered DataFrame containing only specified categories.

    Example:
        >>> filtered = filter_by_category(df, 'iso_code', ['GBR', 'USA', 'DEU'])
    """
    if column not in df.columns:
        return df.head(0)

    return df[df[column].isin(values)].copy()


def apply_filters(df: pd.DataFrame, criteria: dict) -> pd.DataFrame:
    """
    Apply multiple filters based on criteria dictionary.

    Args:
        df: DataFrame to filter.
        criteria: Dictionary with filter criteria:
            - 'countries': List of countries to include
            - 'start_date': Start date for date range
            - 'end_date': End date for date range
            - 'location_column': Column for country filter (default: 'location')
            - 'date_column': Column for date filter (default: 'date')

    Returns:
        Filtered DataFrame matching all criteria.

    Example:
        >>> criteria = {
        ...     'countries': ['United Kingdom', 'Germany'],
        ...     'start_date': datetime(2021, 1, 1),
        ...     'end_date': datetime(2021, 12, 31)
        ... }
        >>> filtered = apply_filters(df, criteria)
    """
    result = df.copy()

    # Apply country filter
    if "countries" in criteria and criteria["countries"]:
        location_col = criteria.get("location_column", "location")
        result = filter_by_country(result, criteria["countries"], location_col)

    # Apply date range filter
    start_date = criteria.get("start_date")
    end_date = criteria.get("end_date")
    if start_date is not None or end_date is not None:
        date_col = criteria.get("date_column", "date")
        result = filter_by_date_range(result, start_date, end_date, date_col)

    # Apply value range filter
    if "value_column" in criteria:
        result = filter_by_value_range(
            result,
            criteria["value_column"],
            criteria.get("min_value"),
            criteria.get("max_value"),
        )

    return result


# ============================================================================
# OOP DataFilter Class (Method Chaining)
# ============================================================================


class DataFilter:
    """
    Fluent data filter with method chaining support.

    OOP Principles Demonstrated:
    - Method chaining (fluent interface)
    - Encapsulation (private _data attribute)
    - Immutability (methods return new instances)

    Example:
        >>> result = (DataFilter(df)
        ...           .by_country('Spain')
        ...           .by_date_range(start=datetime(2021, 1, 1))
        ...           .result())
    """

    def __init__(self, data: pd.DataFrame):
        """
        Initialize DataFilter with a DataFrame.

        Args:
            data: DataFrame to filter
        """
        self._data = data.copy()

    def by_country(self, countries) -> "DataFilter":
        """
        Filter by country.

        Args:
            countries: Country name (str) or list of countries

        Returns:
            New DataFilter instance with filtered data
        """
        # Handle both single country and list
        if isinstance(countries, str):
            countries = [countries]

        filtered = filter_by_country(self._data, countries)
        return DataFilter(filtered)

    def by_date_range(self, start=None, end=None) -> "DataFilter":
        """
        Filter by date range.

        Args:
            start: Start date (inclusive)
            end: End date (inclusive)

        Returns:
            New DataFilter instance with filtered data
        """
        filtered = filter_by_date_range(self._data, start, end)
        return DataFilter(filtered)

    def by_continent(self, continent: str) -> "DataFilter":
        """
        Filter by continent.

        Args:
            continent: Continent name

        Returns:
            New DataFilter instance with filtered data
        """
        if "continent" in self._data.columns:
            filtered = self._data[self._data["continent"] == continent].copy()
        else:
            filtered = self._data.copy()
        return DataFilter(filtered)

    def result(self) -> pd.DataFrame:
        """
        Get the filtered DataFrame.

        Returns:
            Copy of the filtered DataFrame
        """
        return self._data.copy()

    @property
    def count(self) -> int:
        """
        Get the number of rows in filtered data.

        Returns:
            Row count
        """
        return len(self._data)
