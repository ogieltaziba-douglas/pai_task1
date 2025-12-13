"""
Filters Module

This module provides the DataFilter class for filtering public health
vaccination data using OOP method chaining.

Classes:
    DataFilter: OOP class with fluent interface for data filtering
"""

import pandas as pd
from datetime import datetime
from typing import Optional


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

    def by_country(self, countries, column: str = "location") -> "DataFilter":
        """
        Filter by country.

        Args:
            countries: Country name (str) or list of countries
            column: Column name to filter on (default: 'location')

        Returns:
            New DataFilter instance with filtered data
        """
        # Handle both single country and list
        if isinstance(countries, str):
            countries = [countries]

        if column in self._data.columns:
            filtered = self._data[self._data[column].isin(countries)].copy()
        else:
            filtered = self._data.copy()

        return DataFilter(filtered)

    def by_date_range(
        self,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        date_column: str = "date",
    ) -> "DataFilter":
        """
        Filter by date range.

        Args:
            start: Start date (inclusive)
            end: End date (inclusive)
            date_column: Column name for dates (default: 'date')

        Returns:
            New DataFilter instance with filtered data
        """
        result = self._data.copy()

        if date_column in result.columns:
            if start is not None:
                result = result[result[date_column] >= start]
            if end is not None:
                result = result[result[date_column] <= end]

        return DataFilter(result)

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

    def by_value_range(
        self,
        column: str,
        min_val: Optional[float] = None,
        max_val: Optional[float] = None,
    ) -> "DataFilter":
        """
        Filter by numeric value range.

        Args:
            column: Column name to filter on
            min_val: Minimum value (inclusive)
            max_val: Maximum value (inclusive)

        Returns:
            New DataFilter instance with filtered data
        """
        result = self._data.copy()

        if column in result.columns:
            if min_val is not None:
                result = result[result[column] >= min_val]
            if max_val is not None:
                result = result[result[column] <= max_val]

        return DataFilter(result)

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
