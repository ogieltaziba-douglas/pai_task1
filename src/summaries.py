"""
Summaries Module

This module provides functions for generating statistical summaries
and aggregations of public health vaccination data.

Functions:
    calculate_statistics: Calculate basic statistics for a column
    count_by_category: Count occurrences by category
    calculate_trend: Calculate trend information over time
    group_summary: Calculate grouped aggregations
    get_top_n: Get top N records by a column
    get_summary_report: Generate comprehensive summary report
"""

import pandas as pd
import numpy as np
from typing import Optional


def calculate_statistics(df: pd.DataFrame, column: str) -> dict:
    """
    Calculate basic statistics for a numeric column.

    Args:
        df: DataFrame to analyze.
        column: Column name to calculate statistics for.

    Returns:
        Dictionary containing:
            - mean: Average value
            - min: Minimum value
            - max: Maximum value
            - sum: Total sum
            - count: Number of values
            - std: Standard deviation

    Example:
        >>> stats = calculate_statistics(df, 'total_vaccinations')
        >>> print(f"Average: {stats['mean']:,.0f}")
    """
    if column not in df.columns or df.empty:
        return {
            "mean": None,
            "min": None,
            "max": None,
            "sum": None,
            "count": 0,
            "std": None,
        }

    col_data = df[column].dropna()

    if len(col_data) == 0:
        return {
            "mean": None,
            "min": None,
            "max": None,
            "sum": None,
            "count": 0,
            "std": None,
        }

    return {
        "mean": float(col_data.mean()),
        "min": float(col_data.min()),
        "max": float(col_data.max()),
        "sum": float(col_data.sum()),
        "count": int(len(col_data)),
        "std": float(col_data.std()) if len(col_data) > 1 else 0.0,
    }


def count_by_category(df: pd.DataFrame, column: str, sort: bool = True) -> pd.Series:
    """
    Count occurrences by category.

    Args:
        df: DataFrame to analyze.
        column: Column to count by.
        sort: Whether to sort by count descending (default: True).

    Returns:
        Series with category names as index and counts as values.

    Example:
        >>> country_counts = count_by_category(df, 'location')
        >>> print(country_counts.head())
    """
    counts = df[column].value_counts(sort=sort)
    return counts


def calculate_trend(df: pd.DataFrame, date_column: str, value_column: str) -> dict:
    """
    Calculate trend information over time.

    Args:
        df: DataFrame with time series data.
        date_column: Column containing dates.
        value_column: Column containing values to track.

    Returns:
        Dictionary containing:
            - direction: 'increasing', 'decreasing', or 'stable'
            - start_value: First non-null value in series
            - end_value: Last non-null value in series
            - total_change: Absolute change (end - start)
            - percent_change: Percentage change

    Example:
        >>> trend = calculate_trend(df, 'date', 'daily_vaccinations')
        >>> print(f"Trend: {trend['direction']}")
    """
    # Sort by date
    sorted_df = df.sort_values(date_column).copy()

    # Drop NaN values to get meaningful start/end
    valid_data = sorted_df[value_column].dropna()

    if len(valid_data) == 0:
        return {
            "direction": "unknown",
            "start_value": 0.0,
            "end_value": 0.0,
            "total_change": 0.0,
            "percent_change": 0.0,
        }

    # Get first and last non-null values
    start_value = valid_data.iloc[0]
    end_value = valid_data.iloc[-1]

    # Calculate change
    total_change = end_value - start_value
    percent_change = (total_change / start_value * 100) if start_value != 0 else 0

    # Determine direction
    if total_change > 0:
        direction = "increasing"
    elif total_change < 0:
        direction = "decreasing"
    else:
        direction = "stable"

    return {
        "direction": direction,
        "start_value": float(start_value),
        "end_value": float(end_value),
        "total_change": float(total_change),
        "percent_change": float(percent_change),
    }


def group_summary(
    df: pd.DataFrame, group_by: str, agg_column: str, agg_func: str = "sum"
) -> pd.Series:
    """
    Calculate aggregated summary grouped by a column.

    Args:
        df: DataFrame to aggregate.
        group_by: Column to group by.
        agg_column: Column to aggregate.
        agg_func: Aggregation function ('sum', 'mean', 'max', 'min', 'count').

    Returns:
        Series with group names as index and aggregated values.

    Example:
        >>> country_totals = group_summary(df, 'location', 'total_vaccinations', 'sum')
        >>> print(country_totals.head())
    """
    grouped = df.groupby(group_by)[agg_column]

    if agg_func == "sum":
        return grouped.sum()
    elif agg_func == "mean":
        return grouped.mean()
    elif agg_func == "max":
        return grouped.max()
    elif agg_func == "min":
        return grouped.min()
    elif agg_func == "count":
        return grouped.count()
    else:
        raise ValueError(f"Unknown aggregation function: {agg_func}")


def get_top_n(
    df: pd.DataFrame, column: str, n: int = 10, ascending: bool = False
) -> pd.DataFrame:
    """
    Get top N records by a column value.

    Args:
        df: DataFrame to filter.
        column: Column to sort by.
        n: Number of records to return (default: 10).
        ascending: If True, get bottom N instead (default: False).

    Returns:
        DataFrame with top N records.

    Example:
        >>> top_countries = get_top_n(df, 'total_vaccinations', n=10)
        >>> print(top_countries)
    """
    return df.nlargest(n, column) if not ascending else df.nsmallest(n, column)


def get_summary_report(
    df: pd.DataFrame,
    date_column: Optional[str] = None,
    location_column: Optional[str] = None,
) -> dict:
    """
    Generate a comprehensive summary report.

    Args:
        df: DataFrame to summarize.
        date_column: Optional date column for date range info.
        location_column: Optional location column for unique count.

    Returns:
        Dictionary containing:
            - total_records: Number of rows
            - date_range: Dict with min and max dates (if date_column provided)
            - unique_locations: Number of unique locations (if location_column provided)

    Example:
        >>> report = get_summary_report(df, date_column='date', location_column='location')
        >>> print(f"Total records: {report['total_records']}")
    """
    report = {"total_records": len(df)}

    if date_column and date_column in df.columns:
        dates = pd.to_datetime(df[date_column])
        report["date_range"] = {"min": dates.min(), "max": dates.max()}

    if location_column and location_column in df.columns:
        report["unique_locations"] = df[location_column].nunique()

    return report
