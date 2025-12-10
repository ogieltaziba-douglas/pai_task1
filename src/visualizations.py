"""
Visualizations Module

This module provides functions for creating charts and formatted tables
for public health vaccination data.

Functions:
    prepare_chart_data: Prepare data for chart creation
    create_bar_chart: Create bar charts
    create_line_chart: Create line charts for trends
    create_pie_chart: Create pie charts for distribution
    display_table: Format DataFrame as table string
    save_chart: Save chart to file
"""

import pandas as pd
import matplotlib

matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
from typing import List, Optional


def prepare_chart_data(df: pd.DataFrame, x: str, y: str) -> dict:
    """
    Prepare data for chart creation.

    Extracts x and y values from DataFrame columns.

    Args:
        df: DataFrame with data.
        x: Column name for x-axis.
        y: Column name for y-axis.

    Returns:
        Dictionary with 'x' and 'y' lists ready for plotting.

    Example:
        >>> data = prepare_chart_data(df, 'location', 'total_vaccinations')
        >>> print(data['x'])  # Country names
        >>> print(data['y'])  # Vaccination counts
    """
    return {"x": df[x].tolist(), "y": df[y].tolist()}


def create_bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    xlabel: str = None,
    ylabel: str = None,
    figsize: tuple = (10, 6),
    color: str = "steelblue",
) -> plt.Figure:
    """
    Create a bar chart.

    Args:
        df: DataFrame with data.
        x: Column for x-axis categories.
        y: Column for y-axis values.
        title: Chart title.
        xlabel: X-axis label (default: column name).
        ylabel: Y-axis label (default: column name).
        figsize: Figure size tuple (width, height).
        color: Bar color.

    Returns:
        matplotlib Figure object.

    Example:
        >>> fig = create_bar_chart(df, 'location', 'total_vaccinations',
        ...                        'Vaccinations by Country')
        >>> plt.show()
    """
    fig, ax = plt.subplots(figsize=figsize)

    ax.bar(df[x], df[y], color=color)
    ax.set_title(title)
    ax.set_xlabel(xlabel if xlabel else x.replace("_", " ").title())
    ax.set_ylabel(ylabel if ylabel else y.replace("_", " ").title())

    # Rotate x labels if many categories
    if len(df[x]) > 5:
        plt.xticks(rotation=45, ha="right")

    plt.tight_layout()
    return fig


def create_line_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    xlabel: str = None,
    ylabel: str = None,
    figsize: tuple = (10, 6),
    color: str = "steelblue",
    marker: str = "o",
) -> plt.Figure:
    """
    Create a line chart for time series data.

    Args:
        df: DataFrame with data.
        x: Column for x-axis (typically dates).
        y: Column for y-axis values.
        title: Chart title.
        xlabel: X-axis label.
        ylabel: Y-axis label.
        figsize: Figure size tuple.
        color: Line color.
        marker: Marker style for data points.

    Returns:
        matplotlib Figure object.

    Example:
        >>> fig = create_line_chart(df, 'date', 'daily_vaccinations',
        ...                         'Daily Vaccination Trend')
    """
    fig, ax = plt.subplots(figsize=figsize)

    ax.plot(df[x], df[y], color=color, marker=marker, linewidth=2)
    ax.set_title(title)
    ax.set_xlabel(xlabel if xlabel else x.replace("_", " ").title())
    ax.set_ylabel(ylabel if ylabel else y.replace("_", " ").title())

    # Add grid for better readability
    ax.grid(True, linestyle="--", alpha=0.7)

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    return fig


def create_pie_chart(
    labels: List[str],
    values: List[float],
    title: str,
    figsize: tuple = (10, 8),
    autopct: str = "%1.1f%%",
) -> plt.Figure:
    """
    Create a pie chart.

    Args:
        labels: Category labels.
        values: Values for each category.
        title: Chart title.
        figsize: Figure size tuple.
        autopct: Format string for percentage labels.

    Returns:
        matplotlib Figure object.

    Example:
        >>> fig = create_pie_chart(['UK', 'US', 'DE'], [30, 50, 20],
        ...                        'Vaccination Distribution')
    """
    fig, ax = plt.subplots(figsize=figsize)

    ax.pie(values, labels=labels, autopct=autopct, startangle=90)
    ax.set_title(title)
    ax.axis("equal")  # Equal aspect ratio ensures circular pie

    plt.tight_layout()
    return fig


def display_table(df: pd.DataFrame, max_rows: int = None) -> str:
    """
    Format DataFrame as a displayable table string.

    Args:
        df: DataFrame to display.
        max_rows: Maximum rows to show (None for all).

    Returns:
        Formatted string representation of table.

    Example:
        >>> table_str = display_table(df, max_rows=10)
        >>> print(table_str)
    """
    if max_rows is not None:
        display_df = df.head(max_rows)
    else:
        display_df = df

    return display_df.to_string()


def save_chart(fig: plt.Figure, filepath: str, dpi: int = 150) -> bool:
    """
    Save a chart to a file.

    Args:
        fig: matplotlib Figure to save.
        filepath: Path to save file (PNG, JPG, PDF, SVG supported).
        dpi: Resolution in dots per inch.

    Returns:
        True if saved successfully, False otherwise.

    Example:
        >>> fig = create_bar_chart(df, 'location', 'cases', 'Cases')
        >>> save_chart(fig, 'charts/bar_chart.png')
    """
    try:
        fig.savefig(filepath, dpi=dpi, bbox_inches="tight")
        return True
    except Exception as e:
        print(f"Error saving chart: {e}")
        return False
