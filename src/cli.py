"""
CLI Module

This module provides command-line interface functions for the
Public Health Data Insights Dashboard.

Functions:
    get_menu_options: Get available menu options
    validate_menu_choice: Validate user menu selection
    parse_country_input: Parse country names from input
    parse_date_input: Parse date from input string
    format_statistics_output: Format statistics for display
    format_summary_output: Format summary for display
"""

from datetime import datetime
from typing import List, Optional


def get_menu_options() -> dict:
    """
    Get the main menu options.

    Returns:
        Dictionary of menu option number to description.

    Example:
        >>> options = get_menu_options()
        >>> for key, value in options.items():
        ...     print(f"{key}. {value}")
    """
    return {
        "1": "Load data from CSV",
        "2": "View data summary",
        "3": "Filter data by country",
        "4": "Filter data by date range",
        "5": "View statistics",
        "6": "View trends",
        "7": "Generate charts",
        "8": "Export data to CSV",
        "9": "Exit",
    }


def validate_menu_choice(choice: str) -> bool:
    """
    Validate a menu choice input.

    Args:
        choice: User's input string.

    Returns:
        True if valid choice (1-9), False otherwise.

    Example:
        >>> validate_menu_choice('1')
        True
        >>> validate_menu_choice('abc')
        False
    """
    if not choice or not choice.strip():
        return False

    valid_options = get_menu_options().keys()
    return choice.strip() in valid_options


def parse_country_input(input_str: str) -> List[str]:
    """
    Parse country input from user.

    Handles comma-separated country names and strips whitespace.

    Args:
        input_str: Comma-separated country names.

    Returns:
        List of country names (cleaned and stripped).

    Example:
        >>> parse_country_input('United Kingdom, Germany, France')
        ['United Kingdom', 'Germany', 'France']
    """
    if not input_str or not input_str.strip():
        return []

    # Split by comma and strip each country name
    countries = [country.strip() for country in input_str.split(",")]
    # Remove empty strings
    countries = [c for c in countries if c]

    return countries


def parse_date_input(input_str: str) -> Optional[datetime]:
    """
    Parse date input from user.

    Expects date in YYYY-MM-DD format.

    Args:
        input_str: Date string in YYYY-MM-DD format.

    Returns:
        datetime object or None if invalid/empty.

    Example:
        >>> parse_date_input('2021-01-15')
        datetime.datetime(2021, 1, 15, 0, 0)
        >>> parse_date_input('invalid')
        None
    """
    if not input_str or not input_str.strip():
        return None

    try:
        return datetime.strptime(input_str.strip(), "%Y-%m-%d")
    except ValueError:
        return None


def format_statistics_output(stats: dict) -> str:
    """
    Format statistics dictionary for display.

    Args:
        stats: Dictionary with keys like 'mean', 'min', 'max', 'count'.

    Returns:
        Formatted multi-line string for display.

    Example:
        >>> stats = {'mean': 1000, 'min': 500, 'max': 1500}
        >>> print(format_statistics_output(stats))
    """
    lines = ["=" * 40, "Statistics Summary", "=" * 40]

    for key, value in stats.items():
        if value is None:
            formatted_value = "N/A"
        elif isinstance(value, float):
            formatted_value = f"{value:,.2f}"
        elif isinstance(value, int):
            formatted_value = f"{value:,}"
        else:
            formatted_value = str(value)

        # Capitalize key and format nicely
        label = key.replace("_", " ").title()
        lines.append(f"  {label}: {formatted_value}")

    lines.append("=" * 40)
    return "\n".join(lines)


def format_summary_output(summary: dict) -> str:
    """
    Format summary dictionary for display.

    Args:
        summary: Dictionary of summary information.

    Returns:
        Formatted multi-line string for display.

    Example:
        >>> summary = {'total_records': 100, 'unique_locations': 10}
        >>> print(format_summary_output(summary))
    """
    lines = ["=" * 40, "Data Summary", "=" * 40]

    for key, value in summary.items():
        label = key.replace("_", " ").title()

        if isinstance(value, dict):
            # Handle nested dictionaries (like date_range)
            lines.append(f"  {label}:")
            for sub_key, sub_value in value.items():
                sub_label = sub_key.replace("_", " ").title()
                lines.append(f"    {sub_label}: {sub_value}")
        elif isinstance(value, (int, float)):
            lines.append(f"  {label}: {value:,}")
        else:
            lines.append(f"  {label}: {value}")

    lines.append("=" * 40)
    return "\n".join(lines)


def display_menu():
    """Display the main menu to the user."""
    print("\n" + "=" * 50)
    print("  Public Health Data Insights Dashboard")
    print("=" * 50)

    options = get_menu_options()
    for key, value in options.items():
        print(f"  {key}. {value}")

    print("=" * 50)


def get_user_input(prompt: str) -> str:
    """Get input from user with a prompt."""
    return input(f"\n{prompt}: ").strip()
