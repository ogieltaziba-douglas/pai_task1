"""
Test module for summaries.py

Tests cover:
- Statistical calculations (mean, min, max, sum)
- Count aggregations
- Trend calculations over time
- Grouped summaries
- Edge cases (empty data, single value)
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime

from src.summaries import (
    calculate_statistics,
    count_by_category,
    calculate_trend,
    group_summary,
    get_top_n,
    get_summary_report,
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
def time_series_df():
    """Time series data for trend testing."""
    dates = pd.date_range("2021-01-01", periods=10, freq="D")
    return pd.DataFrame(
        {
            "date": dates,
            "daily_vaccinations": [100, 150, 200, 180, 220, 250, 300, 280, 350, 400],
        }
    )


@pytest.fixture
def empty_df():
    """Empty DataFrame for edge case testing."""
    return pd.DataFrame(columns=["location", "total_vaccinations"])


# ============================================================================
# Tests for calculate_statistics()
# ============================================================================


class TestCalculateStatistics:
    """Tests for statistical calculations."""

    def test_calculate_mean(self, vaccination_df):
        """Test mean calculation."""
        result = calculate_statistics(vaccination_df, "total_vaccinations")
        assert "mean" in result
        assert result["mean"] == vaccination_df["total_vaccinations"].mean()

    def test_calculate_min(self, vaccination_df):
        """Test minimum calculation."""
        result = calculate_statistics(vaccination_df, "total_vaccinations")
        assert "min" in result
        assert result["min"] == 500000

    def test_calculate_max(self, vaccination_df):
        """Test maximum calculation."""
        result = calculate_statistics(vaccination_df, "total_vaccinations")
        assert "max" in result
        assert result["max"] == 5000000

    def test_calculate_sum(self, vaccination_df):
        """Test sum calculation."""
        result = calculate_statistics(vaccination_df, "total_vaccinations")
        assert "sum" in result
        assert result["sum"] == vaccination_df["total_vaccinations"].sum()

    def test_calculate_count(self, vaccination_df):
        """Test count calculation."""
        result = calculate_statistics(vaccination_df, "total_vaccinations")
        assert "count" in result
        assert result["count"] == 6

    def test_calculate_std(self, vaccination_df):
        """Test standard deviation calculation."""
        result = calculate_statistics(vaccination_df, "total_vaccinations")
        assert "std" in result

    def test_returns_dict(self, vaccination_df):
        """Test that function returns a dictionary."""
        result = calculate_statistics(vaccination_df, "total_vaccinations")
        assert isinstance(result, dict)

    def test_empty_dataframe(self, empty_df):
        """Test statistics on empty DataFrame."""
        result = calculate_statistics(empty_df, "total_vaccinations")
        assert result["count"] == 0


# ============================================================================
# Tests for count_by_category()
# ============================================================================


class TestCountByCategory:
    """Tests for category counting."""

    def test_count_by_location(self, vaccination_df):
        """Test counting by location."""
        result = count_by_category(vaccination_df, "location")
        assert "United Kingdom" in result.index
        assert result["United Kingdom"] == 2

    def test_count_by_iso_code(self, vaccination_df):
        """Test counting by ISO code."""
        result = count_by_category(vaccination_df, "iso_code")
        assert result["GBR"] == 2
        assert result["DEU"] == 2

    def test_returns_series(self, vaccination_df):
        """Test that function returns a Series."""
        result = count_by_category(vaccination_df, "location")
        assert isinstance(result, pd.Series)

    def test_sorted_by_count(self, vaccination_df):
        """Test that results are sorted by count."""
        result = count_by_category(vaccination_df, "location", sort=True)
        # All have count 2 or 1, so verify descending order
        assert list(result.values) == sorted(result.values, reverse=True)


# ============================================================================
# Tests for calculate_trend()
# ============================================================================


class TestCalculateTrend:
    """Tests for trend calculations."""

    def test_trend_direction_increasing(self, time_series_df):
        """Test detecting increasing trend."""
        result = calculate_trend(time_series_df, "date", "daily_vaccinations")
        assert result["direction"] == "increasing"

    def test_trend_contains_change(self, time_series_df):
        """Test that trend result contains change information."""
        result = calculate_trend(time_series_df, "date", "daily_vaccinations")
        assert "total_change" in result
        assert "percent_change" in result

    def test_trend_start_end_values(self, time_series_df):
        """Test that trend includes start and end values."""
        result = calculate_trend(time_series_df, "date", "daily_vaccinations")
        assert result["start_value"] == 100
        assert result["end_value"] == 400

    def test_returns_dict(self, time_series_df):
        """Test that function returns a dictionary."""
        result = calculate_trend(time_series_df, "date", "daily_vaccinations")
        assert isinstance(result, dict)


# ============================================================================
# Tests for group_summary()
# ============================================================================


class TestGroupSummary:
    """Tests for grouped summaries."""

    def test_group_by_country_sum(self, vaccination_df):
        """Test sum aggregation grouped by country."""
        result = group_summary(
            vaccination_df,
            group_by="location",
            agg_column="total_vaccinations",
            agg_func="sum",
        )
        assert result.loc["United Kingdom"] == 3000000  # 1M + 2M

    def test_group_by_country_mean(self, vaccination_df):
        """Test mean aggregation grouped by country."""
        result = group_summary(
            vaccination_df,
            group_by="location",
            agg_column="total_vaccinations",
            agg_func="mean",
        )
        assert result.loc["United Kingdom"] == 1500000  # (1M + 2M) / 2

    def test_group_by_country_max(self, vaccination_df):
        """Test max aggregation grouped by country."""
        result = group_summary(
            vaccination_df,
            group_by="location",
            agg_column="total_vaccinations",
            agg_func="max",
        )
        assert result.loc["United States"] == 5000000

    def test_returns_series(self, vaccination_df):
        """Test that function returns a Series."""
        result = group_summary(vaccination_df, "location", "total_vaccinations", "sum")
        assert isinstance(result, pd.Series)


# ============================================================================
# Tests for get_top_n()
# ============================================================================


class TestGetTopN:
    """Tests for getting top N values."""

    def test_get_top_3(self, vaccination_df):
        """Test getting top 3 by vaccination count."""
        result = get_top_n(vaccination_df, "total_vaccinations", n=3)
        assert len(result) == 3
        assert result.iloc[0]["total_vaccinations"] == 5000000

    def test_get_bottom_3(self, vaccination_df):
        """Test getting bottom 3 by vaccination count."""
        result = get_top_n(vaccination_df, "total_vaccinations", n=3, ascending=True)
        assert len(result) == 3
        assert result.iloc[0]["total_vaccinations"] == 500000

    def test_returns_dataframe(self, vaccination_df):
        """Test that function returns a DataFrame."""
        result = get_top_n(vaccination_df, "total_vaccinations", n=3)
        assert isinstance(result, pd.DataFrame)


# ============================================================================
# Tests for get_summary_report()
# ============================================================================


class TestGetSummaryReport:
    """Tests for comprehensive summary report."""

    def test_report_contains_total_records(self, vaccination_df):
        """Test that report contains total record count."""
        result = get_summary_report(vaccination_df)
        assert "total_records" in result
        assert result["total_records"] == 6

    def test_report_contains_date_range(self, vaccination_df):
        """Test that report contains date range."""
        result = get_summary_report(vaccination_df, date_column="date")
        assert "date_range" in result

    def test_report_contains_unique_countries(self, vaccination_df):
        """Test that report contains unique country count."""
        result = get_summary_report(vaccination_df, location_column="location")
        assert "unique_locations" in result
        assert result["unique_locations"] == 4

    def test_returns_dict(self, vaccination_df):
        """Test that function returns a dictionary."""
        result = get_summary_report(vaccination_df)
        assert isinstance(result, dict)


# ============================================================================
# Integration Tests
# ============================================================================


class TestSummariesIntegration:
    """Integration tests for summary operations."""

    def test_full_analysis_workflow(self, vaccination_df):
        """Test complete analysis workflow."""
        # Get overall statistics
        stats = calculate_statistics(vaccination_df, "total_vaccinations")
        assert stats["count"] == 6

        # Get counts by country
        country_counts = count_by_category(vaccination_df, "location")
        assert len(country_counts) == 4

        # Get grouped summary
        country_totals = group_summary(
            vaccination_df, "location", "total_vaccinations", "sum"
        )
        assert country_totals["United States"] == 5000000

        # Get top performers
        top_records = get_top_n(vaccination_df, "total_vaccinations", n=2)
        assert len(top_records) == 2
