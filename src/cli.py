"""
CLI Module

This module provides command-line interface functions for the
Public Health Data Insights Dashboard.

Note: This file contains STUBS only. Implementation will follow after
tests are verified to fail (TDD approach).
"""

from datetime import datetime
from typing import List, Optional


def get_menu_options() -> dict:
    """
    Get the main menu options.

    Returns:
        Dictionary of menu option number to description.
    """
    raise NotImplementedError("get_menu_options not yet implemented")


def validate_menu_choice(choice: str) -> bool:
    """
    Validate a menu choice input.

    Args:
        choice: User's input string.

    Returns:
        True if valid choice, False otherwise.
    """
    raise NotImplementedError("validate_menu_choice not yet implemented")


def parse_country_input(input_str: str) -> List[str]:
    """
    Parse country input from user.

    Args:
        input_str: Comma-separated country names.

    Returns:
        List of country names.
    """
    raise NotImplementedError("parse_country_input not yet implemented")


def parse_date_input(input_str: str) -> Optional[datetime]:
    """
    Parse date input from user.

    Args:
        input_str: Date string (YYYY-MM-DD format).

    Returns:
        datetime object or None if invalid.
    """
    raise NotImplementedError("parse_date_input not yet implemented")


def format_statistics_output(stats: dict) -> str:
    """
    Format statistics dictionary for display.

    Args:
        stats: Dictionary of statistics.

    Returns:
        Formatted string for display.
    """
    raise NotImplementedError("format_statistics_output not yet implemented")


def format_summary_output(summary: dict) -> str:
    """
    Format summary dictionary for display.

    Args:
        summary: Dictionary of summary information.

    Returns:
        Formatted string for display.
    """
    raise NotImplementedError("format_summary_output not yet implemented")
