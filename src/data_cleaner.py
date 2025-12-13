"""
Data Cleaner Module

This module provides the DataCleaner class for cleaning and preprocessing
public health vaccination data using OOP method chaining.

Classes:
    DataCleaner: OOP class with fluent interface for data cleaning
"""

import pandas as pd


class DataCleaner:
    """
    Data cleaner class with OOP method chaining support.

    OOP Principles Demonstrated:
    - Method chaining (fluent interface)
    - Encapsulation (private _data attribute)
    - Immutability (methods return new instances)

    Example:
        >>> cleaned = (DataCleaner(raw_data)
        ...            .fill_missing(value=0)
        ...            .convert_dates(['date'])
        ...            .remove_duplicates()
        ...            .result())
    """

    def __init__(self, data: pd.DataFrame):
        """
        Initialize DataCleaner with data.

        Args:
            data: DataFrame to clean
        """
        self._data = data.copy()

    def fill_missing(self, value=None, strategy: str = None) -> "DataCleaner":
        """
        Fill missing values.

        Args:
            value: Value to fill with (if specified)
            strategy: Strategy ('mean', 'median') for numeric columns

        Returns:
            New DataCleaner with filled values
        """
        result = self._data.copy()

        if value is not None:
            # Fill all columns with specified value
            result = result.fillna(value)
        elif strategy == "mean":
            # Fill numeric columns with mean
            for col in result.select_dtypes(include=["number"]).columns:
                result[col] = result[col].fillna(result[col].mean())
        elif strategy == "median":
            # Fill numeric columns with median
            for col in result.select_dtypes(include=["number"]).columns:
                result[col] = result[col].fillna(result[col].median())

        return DataCleaner(result)

    def convert_dates(self, columns: list) -> "DataCleaner":
        """
        Convert columns to datetime.

        Args:
            columns: List of column names to convert

        Returns:
            New DataCleaner with converted dates
        """
        result = self._data.copy()
        for col in columns:
            if col in result.columns:
                result[col] = pd.to_datetime(result[col], errors="coerce")
        return DataCleaner(result)

    def remove_duplicates(self, subset: list = None) -> "DataCleaner":
        """
        Remove duplicate rows.

        Args:
            subset: Columns to consider for duplicates

        Returns:
            New DataCleaner with duplicates removed
        """
        result = self._data.drop_duplicates(subset=subset)
        return DataCleaner(result)

    def result(self) -> pd.DataFrame:
        """
        Get the cleaned data.

        Returns:
            Cleaned DataFrame (copy for encapsulation)
        """
        return self._data.copy()

    @property
    def count(self) -> int:
        """
        Get row count.

        Returns:
            Number of rows
        """
        return len(self._data)
