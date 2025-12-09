"""
Data Loader Module

This module provides functions for loading public health data from various
file formats (CSV, JSON) into pandas DataFrames.

Functions:
    load_csv: Load data from CSV files
    load_json: Load data from JSON files
    validate_data_structure: Check if required columns exist
    get_data_info: Get summary information about loaded data
"""

import pandas as pd
import json
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


def load_json(filepath: str) -> pd.DataFrame:
    """
    Load data from a JSON file into a pandas DataFrame.

    Reads a JSON file containing an array of objects and returns
    its contents as a pandas DataFrame.

    Args:
        filepath: Path to the JSON file to load.

    Returns:
        pandas DataFrame containing the loaded data.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If the JSON is malformed or cannot be parsed.

    Example:
        >>> df = load_json('data/vaccinations.json')
        >>> print(df.head())
    """
    # Check if file exists first
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    # Try to load and parse JSON
    try:
        with open(filepath, "r") as f:
            data = json.load(f)

        # Convert to DataFrame
        df = pd.DataFrame(data)
        return df

    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}")


def validate_data_structure(df: pd.DataFrame, required_columns: list) -> bool:
    """
    Validate that a DataFrame contains the required columns.

    Checks if all specified columns exist in the DataFrame.
    Useful for ensuring data integrity after loading.

    Args:
        df: The DataFrame to validate.
        required_columns: List of column names that must be present.

    Returns:
        True if all required columns are present, False otherwise.
        Returns True if required_columns is empty.
        Returns False if DataFrame is empty and columns are required.

    Example:
        >>> df = load_csv('data/vaccinations.csv')
        >>> is_valid = validate_data_structure(df, ['location', 'date'])
        >>> print(f"Data valid: {is_valid}")
    """
    # If no columns are required, validation passes
    if not required_columns:
        return True

    # If DataFrame has no columns, validation fails if columns are required
    if df.empty and len(df.columns) == 0:
        return False

    # Check if all required columns exist
    existing_columns = set(df.columns)
    required_set = set(required_columns)

    return required_set.issubset(existing_columns)


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
