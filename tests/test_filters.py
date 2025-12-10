"""
Test module for filters.py

Tests cover:
- Filtering by country/region
- Filtering by date range
- Filtering by category/value
- Combined filters
- Edge cases (no matches, invalid criteria)
"""

import pytest
import pandas as pd
from datetime import datetime

from src.filters import (
    filter_by_country,
    filter_by_date_range,
    filter_by_value_range,
    filter_by_category,
    apply_filters,
)


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def vaccination_df():
    """Sample vaccination data for testing."""
    return pd.DataFrame(
        {
            "location": [
                "United Kingdom",
                "United States",
                "Germany",
                "France",
                "United Kingdom",
                "Germany",
            ],
            "iso_code": ["GBR", "USA", "DEU", "FRA", "GBR", "DEU"],
            "date": pd.to_datetime(
                [
                    "2021-01-01",
                    "2021-01-15",
                    "2021-02-01",
                    "2021-02-15",
                    "2021-03-01",
                    "2021-03-15",
                ]
            ),
            "total_vaccinations": [1000000, 5000000, 500000, 750000, 2000000, 1000000],
            "people_vaccinated": [800000, 4000000, 400000, 600000, 1600000, 800000],
            "daily_vaccinations": [50000, 100000, 25000, 35000, 60000, 45000],
        }
    )


@pytest.fixture
def empty_df():
    """Empty DataFrame for testing edge cases."""
    return pd.DataFrame(columns=["location", "date", "total_vaccinations"])


# ============================================================================
# Tests for filter_by_country()
# ============================================================================


class TestFilterByCountry:
    """Tests for country filtering."""

    def test_filter_single_country(self, vaccination_df):
        """Test filtering by a single country."""
        result = filter_by_country(vaccination_df, ["United Kingdom"])
        assert len(result) == 2
        assert all(result["location"] == "United Kingdom")

    def test_filter_multiple_countries(self, vaccination_df):
        """Test filtering by multiple countries."""
        result = filter_by_country(vaccination_df, ["United Kingdom", "Germany"])
        assert len(result) == 4
        assert set(result["location"].unique()) == {"United Kingdom", "Germany"}

    def test_filter_by_iso_code(self, vaccination_df):
        """Test filtering by ISO code."""
        result = filter_by_country(vaccination_df, ["USA"], column="iso_code")
        assert len(result) == 1
        assert result.iloc[0]["location"] == "United States"

    def test_filter_no_matches(self, vaccination_df):
        """Test filtering with no matches returns empty DataFrame."""
        result = filter_by_country(vaccination_df, ["Japan"])
        assert len(result) == 0
        assert isinstance(result, pd.DataFrame)

    def test_filter_returns_dataframe(self, vaccination_df):
        """Test that filter returns a DataFrame."""
        result = filter_by_country(vaccination_df, ["Germany"])
        assert isinstance(result, pd.DataFrame)

    def test_filter_empty_dataframe(self, empty_df):
        """Test filtering an empty DataFrame."""
        result = filter_by_country(empty_df, ["United Kingdom"])
        assert len(result) == 0


# ============================================================================
# Tests for filter_by_date_range()
# ============================================================================


class TestFilterByDateRange:
    """Tests for date range filtering."""

    def test_filter_date_range(self, vaccination_df):
        """Test filtering by date range."""
        start = datetime(2021, 1, 1)
        end = datetime(2021, 1, 31)
        result = filter_by_date_range(vaccination_df, start, end)
        assert len(result) == 2  # Jan 1 and Jan 15

    def test_filter_start_date_only(self, vaccination_df):
        """Test filtering with only start date."""
        start = datetime(2021, 3, 1)
        result = filter_by_date_range(vaccination_df, start_date=start)
        assert len(result) == 2  # Mar 1 and Mar 15

    def test_filter_end_date_only(self, vaccination_df):
        """Test filtering with only end date."""
        end = datetime(2021, 1, 31)
        result = filter_by_date_range(vaccination_df, end_date=end)
        assert len(result) == 2  # Jan 1 and Jan 15

    def test_filter_date_range_inclusive(self, vaccination_df):
        """Test that date range is inclusive."""
        start = datetime(2021, 1, 1)
        end = datetime(2021, 1, 1)
        result = filter_by_date_range(vaccination_df, start, end)
        assert len(result) == 1

    def test_filter_no_dates_in_range(self, vaccination_df):
        """Test filtering with no matching dates."""
        start = datetime(2022, 1, 1)
        end = datetime(2022, 12, 31)
        result = filter_by_date_range(vaccination_df, start, end)
        assert len(result) == 0

    def test_filter_returns_dataframe(self, vaccination_df):
        """Test that filter returns a DataFrame."""
        result = filter_by_date_range(vaccination_df, datetime(2021, 1, 1))
        assert isinstance(result, pd.DataFrame)


# ============================================================================
# Tests for filter_by_value_range()
# ============================================================================


class TestFilterByValueRange:
    """Tests for value range filtering."""

    def test_filter_min_value(self, vaccination_df):
        """Test filtering by minimum value."""
        result = filter_by_value_range(
            vaccination_df, "total_vaccinations", min_val=1000000
        )
        assert len(result) == 3  # Values >= 1000000
        assert all(result["total_vaccinations"] >= 1000000)

    def test_filter_max_value(self, vaccination_df):
        """Test filtering by maximum value."""
        result = filter_by_value_range(
            vaccination_df, "total_vaccinations", max_val=750000
        )
        assert all(result["total_vaccinations"] <= 750000)

    def test_filter_value_range(self, vaccination_df):
        """Test filtering by both min and max value."""
        result = filter_by_value_range(
            vaccination_df, "total_vaccinations", min_val=500000, max_val=1000000
        )
        assert all(
            (result["total_vaccinations"] >= 500000)
            & (result["total_vaccinations"] <= 1000000)
        )

    def test_filter_no_values_in_range(self, vaccination_df):
        """Test filtering with no matching values."""
        result = filter_by_value_range(
            vaccination_df, "total_vaccinations", min_val=10000000
        )
        assert len(result) == 0


# ============================================================================
# Tests for filter_by_category()
# ============================================================================


class TestFilterByCategory:
    """Tests for category filtering."""

    def test_filter_single_value(self, vaccination_df):
        """Test filtering by single category value."""
        result = filter_by_category(vaccination_df, "iso_code", ["GBR"])
        assert len(result) == 2

    def test_filter_multiple_values(self, vaccination_df):
        """Test filtering by multiple category values."""
        result = filter_by_category(vaccination_df, "iso_code", ["GBR", "DEU"])
        assert len(result) == 4

    def test_filter_no_matches(self, vaccination_df):
        """Test filtering with no matching categories."""
        result = filter_by_category(vaccination_df, "iso_code", ["JPN"])
        assert len(result) == 0


# ============================================================================
# Tests for apply_filters()
# ============================================================================


class TestApplyFilters:
    """Tests for combined filter application."""

    def test_apply_country_filter(self, vaccination_df):
        """Test applying country filter via apply_filters."""
        criteria = {"countries": ["United Kingdom"]}
        result = apply_filters(vaccination_df, criteria)
        assert len(result) == 2

    def test_apply_date_filter(self, vaccination_df):
        """Test applying date filter via apply_filters."""
        criteria = {
            "start_date": datetime(2021, 2, 1),
            "end_date": datetime(2021, 2, 28),
        }
        result = apply_filters(vaccination_df, criteria)
        assert len(result) == 2  # Feb 1 and Feb 15

    def test_apply_combined_filters(self, vaccination_df):
        """Test applying multiple filters together."""
        criteria = {
            "countries": ["United Kingdom", "Germany"],
            "start_date": datetime(2021, 2, 1),
        }
        result = apply_filters(vaccination_df, criteria)
        # UK Mar 1, Germany Feb 1, Germany Mar 15
        assert len(result) == 3

    def test_apply_empty_criteria(self, vaccination_df):
        """Test that empty criteria returns all data."""
        result = apply_filters(vaccination_df, {})
        assert len(result) == len(vaccination_df)

    def test_apply_filters_returns_dataframe(self, vaccination_df):
        """Test that apply_filters returns a DataFrame."""
        result = apply_filters(vaccination_df, {})
        assert isinstance(result, pd.DataFrame)


# ============================================================================
# Integration Tests
# ============================================================================


class TestFiltersIntegration:
    """Integration tests for filtering operations."""

    def test_chain_multiple_filters(self, vaccination_df):
        """Test chaining multiple filter operations."""
        # First filter by country
        result = filter_by_country(vaccination_df, ["United Kingdom", "Germany"])
        # Then filter by date
        result = filter_by_date_range(result, datetime(2021, 2, 1))
        # Then filter by value
        result = filter_by_value_range(result, "total_vaccinations", min_val=1000000)

        assert len(result) == 2  # UK Mar 1 and Germany Mar 15
