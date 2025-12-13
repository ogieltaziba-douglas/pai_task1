"""
Data Loader Module

This module provides functions for loading public health data from
CSV files into pandas DataFrames.

Functions:
    load_csv: Load data from CSV files
    get_data_info: Get summary information about loaded data
"""

import pandas as pd
import os


def load_csv(filepath: str) -> pd.DataFrame:
    """
    Load data from a CSV file into a pandas DataFrame.

    Reads a CSV file and returns its contents as a pandas DataFrame.
    Handles empty files by returning an empty DataFrame.

    Args:
        filepath: Path to the CSV file to load.

    Returns:
        pandas DataFrame containing the loaded data.
        Returns empty DataFrame if file is empty.

    Raises:
        FileNotFoundError: If the specified file does not exist.

    Example:
        >>> df = load_csv('data/vaccinations.csv')
        >>> print(df.head())
    """
    # Check if file exists first
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    # Check if file is empty
    if os.path.getsize(filepath) == 0:
        return pd.DataFrame()

    # Load and return the CSV data
    try:
        df = pd.read_csv(filepath)
        return df
    except pd.errors.EmptyDataError:
        # Handle case where file has no parseable data
        return pd.DataFrame()


def get_data_info(df: pd.DataFrame) -> dict:
    """
    Get summary information about a DataFrame.

    Provides a quick overview of the DataFrame including size,
    column names, and missing value counts.

    Args:
        df: The DataFrame to summarize.

    Returns:
        Dictionary containing:
        - row_count: Number of rows in the DataFrame
        - column_count: Number of columns in the DataFrame
        - columns: List of column names
        - missing_values: Total count of missing (NaN) values

    Example:
        >>> df = load_csv('data/vaccinations.csv')
        >>> info = get_data_info(df)
        >>> print(f"Loaded {info['row_count']} records")
    """
    info = {
        "row_count": len(df),
        "column_count": len(df.columns),
        "columns": list(df.columns),
        "missing_values": int(df.isna().sum().sum()),
    }

    return info
