"""
Test module for cli.py

Tests cover:
- Menu display
- User input validation
- Command parsing
- Output formatting
"""

import pytest
from io import StringIO

from src.cli import (
    get_menu_options,
    validate_menu_choice,
    parse_country_input,
    parse_date_input,
    format_statistics_output,
    format_summary_output,
)


# ============================================================================
# Tests for get_menu_options()
# ============================================================================


class TestGetMenuOptions:
    """Tests for menu options."""

    def test_returns_dict(self):
        """Test that get_menu_options returns a dictionary."""
        result = get_menu_options()
        assert isinstance(result, dict)

    def test_contains_required_options(self):
        """Test that menu contains required options."""
        result = get_menu_options()
        assert "1" in result or 1 in result
        assert len(result) >= 5  # Should have multiple menu items


# ============================================================================
# Tests for validate_menu_choice()
# ============================================================================


class TestValidateMenuChoice:
    """Tests for menu choice validation."""

    def test_valid_choice(self):
        """Test valid menu choices."""
        assert validate_menu_choice("1") is True
        assert validate_menu_choice("5") is True

    def test_invalid_choice_letter(self):
        """Test invalid letter input."""
        assert validate_menu_choice("abc") is False

    def test_invalid_choice_out_of_range(self):
        """Test out of range choice."""
        assert validate_menu_choice("99") is False

    def test_empty_input(self):
        """Test empty input."""
        assert validate_menu_choice("") is False


# ============================================================================
# Tests for parse_country_input()
# ============================================================================


class TestParseCountryInput:
    """Tests for country input parsing."""

    def test_single_country(self):
        """Test parsing single country."""
        result = parse_country_input("United Kingdom")
        assert result == ["United Kingdom"]

    def test_multiple_countries_comma(self):
        """Test parsing comma-separated countries."""
        result = parse_country_input("United Kingdom, United States, Germany")
        assert len(result) == 3
        assert "United Kingdom" in result
        assert "Germany" in result

    def test_strips_whitespace(self):
        """Test that whitespace is stripped."""
        result = parse_country_input("  United Kingdom  ,  Germany  ")
        assert result == ["United Kingdom", "Germany"]

    def test_empty_input(self):
        """Test empty input returns empty list."""
        result = parse_country_input("")
        assert result == []


# ============================================================================
# Tests for parse_date_input()
# ============================================================================


class TestParseDateInput:
    """Tests for date input parsing."""

    def test_valid_date(self):
        """Test parsing valid date."""
        result = parse_date_input("2021-01-15")
        assert result is not None
        assert result.year == 2021
        assert result.month == 1
        assert result.day == 15

    def test_invalid_date(self):
        """Test parsing invalid date returns None."""
        result = parse_date_input("not-a-date")
        assert result is None

    def test_empty_input(self):
        """Test empty input returns None."""
        result = parse_date_input("")
        assert result is None


# ============================================================================
# Tests for format_statistics_output()
# ============================================================================


class TestFormatStatisticsOutput:
    """Tests for statistics output formatting."""

    def test_returns_string(self):
        """Test that function returns a string."""
        stats = {"mean": 1000, "min": 500, "max": 1500, "count": 10}
        result = format_statistics_output(stats)
        assert isinstance(result, str)

    def test_contains_values(self):
        """Test that output contains stat values."""
        stats = {"mean": 1000, "min": 500, "max": 1500, "count": 10}
        result = format_statistics_output(stats)
        assert "1000" in result or "1,000" in result

    def test_handles_none_values(self):
        """Test handling of None values."""
        stats = {"mean": None, "min": None, "max": None, "count": 0}
        result = format_statistics_output(stats)
        assert isinstance(result, str)


# ============================================================================
# Tests for format_summary_output()
# ============================================================================


class TestFormatSummaryOutput:
    """Tests for summary output formatting."""

    def test_returns_string(self):
        """Test that function returns a string."""
        summary = {"total_records": 100, "unique_locations": 10}
        result = format_summary_output(summary)
        assert isinstance(result, str)

    def test_contains_labels(self):
        """Test that output contains descriptive labels."""
        summary = {"total_records": 100}
        result = format_summary_output(summary)
        # Should have some label/description
        assert len(result) > 0
