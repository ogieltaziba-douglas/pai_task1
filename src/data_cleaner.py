"""
Data Cleaner Module

This module provides functions for cleaning and preprocessing
public health vaccination data.

Functions:
    handle_missing_values: Handle NaN values with various strategies
    convert_dates: Convert string columns to datetime
    convert_numeric: Convert string columns to numeric
    standardize_text: Standardize text formatting
    remove_duplicates: Remove duplicate rows
    validate_data_range: Validate values are within expected range
    clean_dataframe: Apply comprehensive cleaning
"""

import pandas as pd
import numpy as np


def handle_missing_values(
    df: pd.DataFrame, strategy: str = "drop", fill_value=None, columns: list = None
) -> pd.DataFrame:
    """
    Handle missing values in a DataFrame.

    Args:
        df: DataFrame to clean.
        strategy: How to handle missing values:
            - 'drop': Remove rows with missing values
            - 'fill': Fill with specified fill_value
            - 'mean': Fill numeric columns with mean
            - 'median': Fill numeric columns with median
        fill_value: Value to use when strategy is 'fill'.
        columns: Specific columns to apply to. If None, applies to all.

    Returns:
        DataFrame with missing values handled.

    Example:
        >>> df = handle_missing_values(df, strategy='fill', fill_value=0)
        >>> df = handle_missing_values(df, strategy='mean')
    """
    # Work on a copy to avoid modifying original
    result = df.copy()

    # Determine which columns to process
    target_columns = columns if columns else result.columns.tolist()

    if strategy == "drop":
        # Drop rows with any missing values in target columns
        result = result.dropna(subset=target_columns)

    elif strategy == "fill":
        # Fill with specified value
        for col in target_columns:
            if col in result.columns:
                result[col] = result[col].fillna(fill_value)

    elif strategy == "mean":
        # Fill numeric columns with mean
        for col in target_columns:
            if col in result.columns and pd.api.types.is_numeric_dtype(result[col]):
                result[col] = result[col].fillna(result[col].mean())

    elif strategy == "median":
        # Fill numeric columns with median
        for col in target_columns:
            if col in result.columns and pd.api.types.is_numeric_dtype(result[col]):
                result[col] = result[col].fillna(result[col].median())

    return result


def convert_dates(
    df: pd.DataFrame, columns: list, format: str = None, errors: str = "raise"
) -> pd.DataFrame:
    """
    Convert string columns to datetime.

    Args:
        df: DataFrame to process.
        columns: List of column names to convert.
        format: Date format string (optional, e.g., '%Y-%m-%d').
        errors: How to handle errors:
            - 'raise': Raise exception on invalid date
            - 'coerce': Set invalid dates to NaT
            - 'ignore': Return original value

    Returns:
        DataFrame with converted date columns.

    Example:
        >>> df = convert_dates(df, columns=['date'], format='%Y-%m-%d')
    """
    result = df.copy()

    for col in columns:
        if col in result.columns:
            result[col] = pd.to_datetime(result[col], format=format, errors=errors)

    return result


def convert_numeric(
    df: pd.DataFrame, columns: list, errors: str = "raise"
) -> pd.DataFrame:
    """
    Convert string columns to numeric.

    Args:
        df: DataFrame to process.
        columns: List of column names to convert.
        errors: How to handle errors:
            - 'raise': Raise exception on invalid value
            - 'coerce': Set invalid values to NaN
            - 'ignore': Return original value

    Returns:
        DataFrame with converted numeric columns.

    Example:
        >>> df = convert_numeric(df, columns=['cases', 'deaths'])
    """
    result = df.copy()

    for col in columns:
        if col in result.columns:
            result[col] = pd.to_numeric(result[col], errors=errors)

    return result


def standardize_text(df: pd.DataFrame, columns: list, case: str = None) -> pd.DataFrame:
    """
    Standardize text in string columns.

    Strips whitespace and optionally converts case.

    Args:
        df: DataFrame to process.
        columns: List of column names to standardize.
        case: Case transformation:
            - 'lower': Convert to lowercase
            - 'upper': Convert to uppercase
            - 'title': Convert to title case
            - None: No case conversion

    Returns:
        DataFrame with standardized text columns.

    Example:
        >>> df = standardize_text(df, columns=['location'], case='title')
    """
    result = df.copy()

    for col in columns:
        if col in result.columns and result[col].dtype == "object":
            # Strip whitespace
            result[col] = result[col].str.strip()

            # Apply case transformation
            if case == "lower":
                result[col] = result[col].str.lower()
            elif case == "upper":
                result[col] = result[col].str.upper()
            elif case == "title":
                result[col] = result[col].str.title()

    return result


def remove_duplicates(
    df: pd.DataFrame, subset: list = None, keep: str = "first"
) -> pd.DataFrame:
    """
    Remove duplicate rows from DataFrame.

    Args:
        df: DataFrame to process.
        subset: Column names to consider for identifying duplicates.
                If None, all columns are used.
        keep: Which duplicate to keep:
            - 'first': Keep first occurrence
            - 'last': Keep last occurrence
            - False: Drop all duplicates

    Returns:
        DataFrame with duplicates removed.

    Example:
        >>> df = remove_duplicates(df, subset=['location', 'date'])
    """
    return df.drop_duplicates(subset=subset, keep=keep)


def validate_data_range(
    df: pd.DataFrame, column: str, min_val=None, max_val=None
) -> dict:
    """
    Validate that values in a column fall within a specified range.

    Args:
        df: DataFrame to validate.
        column: Column name to check.
        min_val: Minimum allowed value (inclusive).
        max_val: Maximum allowed value (inclusive).

    Returns:
        Dictionary containing:
            - valid: True if all values are within range
            - out_of_range_count: Number of values outside range
            - min_value: Actual minimum in the column
            - max_value: Actual maximum in the column

    Example:
        >>> result = validate_data_range(df, 'cases', min_val=0, max_val=1000000)
        >>> if not result['valid']:
        >>>     print(f"Found {result['out_of_range_count']} invalid values")
    """
    if column not in df.columns:
        return {
            "valid": False,
            "out_of_range_count": 0,
            "error": f"Column {column} not found",
        }

    col_data = df[column].dropna()

    out_of_range = 0
    if min_val is not None:
        out_of_range += (col_data < min_val).sum()
    if max_val is not None:
        out_of_range += (col_data > max_val).sum()

    return {
        "valid": bool(out_of_range == 0),
        "out_of_range_count": int(out_of_range),
        "min_value": col_data.min() if len(col_data) > 0 else None,
        "max_value": col_data.max() if len(col_data) > 0 else None,
    }


def clean_dataframe(
    df: pd.DataFrame, fill_missing: bool = False, fill_value=None
) -> pd.DataFrame:
    """
    Apply comprehensive cleaning to a DataFrame.

    Performs the following operations:
    1. Remove duplicate rows
    2. Optionally fill missing values in numeric columns

    Args:
        df: DataFrame to clean.
        fill_missing: Whether to fill missing values in numeric columns.
        fill_value: Value to fill missing with. If None, uses 0.

    Returns:
        Cleaned DataFrame.

    Example:
        >>> clean_df = clean_dataframe(df, fill_missing=True, fill_value=0)
    """
    result = df.copy()

    # Remove duplicates
    result = remove_duplicates(result)

    # Handle missing values in numeric columns
    if fill_missing:
        numeric_cols = result.select_dtypes(include=[np.number]).columns.tolist()
        fill_val = fill_value if fill_value is not None else 0
        result = handle_missing_values(
            result, strategy="fill", fill_value=fill_val, columns=numeric_cols
        )

    return result


# ============================================================================
# OOP DataCleaner Class (Method Chaining)
# ============================================================================


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
        raise NotImplementedError("DataCleaner.__init__ not implemented")

    def fill_missing(self, value=None, strategy: str = None) -> "DataCleaner":
        """
        Fill missing values.

        Args:
            value: Value to fill with (if specified)
            strategy: Strategy ('mean', 'median') for numeric columns

        Returns:
            New DataCleaner with filled values
        """
        raise NotImplementedError("DataCleaner.fill_missing not implemented")

    def convert_dates(self, columns: list) -> "DataCleaner":
        """
        Convert columns to datetime.

        Args:
            columns: List of column names to convert

        Returns:
            New DataCleaner with converted dates
        """
        raise NotImplementedError("DataCleaner.convert_dates not implemented")

    def remove_duplicates(self, subset: list = None) -> "DataCleaner":
        """
        Remove duplicate rows.

        Args:
            subset: Columns to consider for duplicates

        Returns:
            New DataCleaner with duplicates removed
        """
        raise NotImplementedError("DataCleaner.remove_duplicates not implemented")

    def result(self) -> pd.DataFrame:
        """
        Get the cleaned data.

        Returns:
            Cleaned DataFrame (copy for encapsulation)
        """
        raise NotImplementedError("DataCleaner.result not implemented")

    @property
    def count(self) -> int:
        """
        Get row count.

        Returns:
            Number of rows
        """
        raise NotImplementedError("DataCleaner.count not implemented")
