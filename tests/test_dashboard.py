"""
Tests for Dashboard Module

Tests for business logic and data operations.
"""

import pytest
import pandas as pd
from unittest.mock import patch, MagicMock


class TestDashboardState:
    """Tests for DashboardState class."""

    def test_dashboard_state_exists(self):
        """Test that DashboardState class is defined."""
        from src.dashboard import DashboardState

        assert DashboardState is not None

    def test_dashboard_state_init(self):
        """Test that DashboardState can be initialized."""
        from src.dashboard import DashboardState

        state = DashboardState()
        assert state is not None

    def test_dashboard_state_has_current_data(self):
        """Test that DashboardState has current_data attribute."""
        from src.dashboard import DashboardState

        state = DashboardState()
        assert hasattr(state, "current_data")
        assert state.current_data is None

    def test_dashboard_state_has_db_connection(self):
        """Test that DashboardState has db_connection attribute."""
        from src.dashboard import DashboardState

        state = DashboardState()
        assert hasattr(state, "db_connection")
        assert state.db_connection is None


class TestGetCountriesOnly:
    """Tests for get_countries_only function."""

    def test_get_countries_only_exists(self):
        """Test that get_countries_only function is defined."""
        from src.dashboard import get_countries_only

        assert get_countries_only is not None

    def test_get_countries_only_filters_world(self):
        """Test that World is filtered out."""
        from src.dashboard import get_countries_only

        df = pd.DataFrame(
            {
                "location": ["United Kingdom", "World", "Germany"],
                "value": [100, 1000, 200],
            }
        )
        result = get_countries_only(df)
        assert "World" not in result["location"].values
        assert len(result) == 2

    def test_get_countries_only_filters_income_groups(self):
        """Test that income groups are filtered out."""
        from src.dashboard import get_countries_only

        df = pd.DataFrame(
            {
                "location": ["Brazil", "High income", "Low income"],
                "value": [100, 1000, 500],
            }
        )
        result = get_countries_only(df)
        assert len(result) == 1
        assert "Brazil" in result["location"].values


class TestLoadData:
    """Tests for load_data function."""

    def test_load_data_exists(self):
        """Test that load_data function is defined."""
        from src.dashboard import load_data

        assert load_data is not None

    def test_load_data_returns_dict(self):
        """Test that load_data returns a result dictionary."""
        from src.dashboard import load_data, DashboardState

        state = DashboardState()

        with patch("src.dashboard.load_csv") as mock_load:
            mock_load.return_value = pd.DataFrame(
                {
                    "location": ["UK"],
                    "date": ["2021-01-01"],
                    "total_vaccinations": [1000],
                }
            )
            result = load_data(state)
            assert isinstance(result, dict)
            assert "success" in result

    def test_load_data_updates_state(self):
        """Test that load_data updates state.current_data."""
        from src.dashboard import load_data, DashboardState

        state = DashboardState()

        test_df = pd.DataFrame(
            {"location": ["UK"], "date": ["2021-01-01"], "total_vaccinations": [1000]}
        )

        with patch("src.dashboard.load_csv", return_value=test_df):
            load_data(state)
            assert state.current_data is not None


class TestGetSummary:
    """Tests for get_summary function."""

    def test_get_summary_exists(self):
        """Test that get_summary function is defined."""
        from src.dashboard import get_summary

        assert get_summary is not None

    def test_get_summary_returns_dict(self):
        """Test that get_summary returns a dictionary."""
        from src.dashboard import get_summary, DashboardState

        state = DashboardState()
        state.current_data = pd.DataFrame(
            {
                "location": ["UK", "Germany"],
                "date": pd.to_datetime(["2021-01-01", "2021-01-02"]),
                "total_vaccinations": [1000, 2000],
            }
        )
        result = get_summary(state)
        assert isinstance(result, dict)

    def test_get_summary_has_total_records(self):
        """Test that summary includes total_records."""
        from src.dashboard import get_summary, DashboardState

        state = DashboardState()
        state.current_data = pd.DataFrame(
            {
                "location": ["UK", "Germany"],
                "date": pd.to_datetime(["2021-01-01", "2021-01-02"]),
                "total_vaccinations": [1000, 2000],
            }
        )
        result = get_summary(state)
        assert "total_records" in result
        assert result["total_records"] == 2


class TestGetStatistics:
    """Tests for get_statistics function."""

    def test_get_statistics_exists(self):
        """Test that get_statistics function is defined."""
        from src.dashboard import get_statistics

        assert get_statistics is not None

    def test_get_statistics_returns_dict(self):
        """Test that get_statistics returns a dictionary."""
        from src.dashboard import get_statistics, DashboardState

        state = DashboardState()
        state.current_data = pd.DataFrame(
            {"location": ["UK", "Germany"], "total_vaccinations": [1000, 2000]}
        )
        result = get_statistics(state, "total_vaccinations")
        assert isinstance(result, dict)

    def test_get_statistics_has_mean(self):
        """Test that statistics includes mean."""
        from src.dashboard import get_statistics, DashboardState

        state = DashboardState()
        state.current_data = pd.DataFrame(
            {"location": ["UK", "Germany"], "total_vaccinations": [1000, 2000]}
        )
        result = get_statistics(state, "total_vaccinations")
        assert "mean" in result


class TestGetTrendAnalysis:
    """Tests for get_trend_analysis function."""

    def test_get_trend_analysis_exists(self):
        """Test that get_trend_analysis function is defined."""
        from src.dashboard import get_trend_analysis

        assert get_trend_analysis is not None

    def test_get_trend_analysis_returns_dict(self):
        """Test that get_trend_analysis returns a dictionary."""
        from src.dashboard import get_trend_analysis, DashboardState

        state = DashboardState()
        state.current_data = pd.DataFrame(
            {
                "location": ["UK", "UK", "UK"],
                "date": pd.to_datetime(["2021-01-01", "2021-01-02", "2021-01-03"]),
                "daily_vaccinations": [100, 200, 300],
            }
        )
        result = get_trend_analysis(state, "United Kingdom")
        assert isinstance(result, dict)

    def test_get_trend_analysis_has_direction(self):
        """Test that trend analysis includes direction."""
        from src.dashboard import get_trend_analysis, DashboardState

        state = DashboardState()
        state.current_data = pd.DataFrame(
            {
                "location": ["UK", "UK", "UK"],
                "date": pd.to_datetime(["2021-01-01", "2021-01-02", "2021-01-03"]),
                "daily_vaccinations": [100, 200, 300],
            }
        )
        result = get_trend_analysis(state, "UK")
        assert "direction" in result


class TestFilterDataByCountry:
    """Tests for filter_data_by_country function."""

    def test_filter_data_by_country_exists(self):
        """Test that filter_data_by_country function is defined."""
        from src.dashboard import filter_data_by_country

        assert filter_data_by_country is not None

    def test_filter_data_by_country_returns_dataframe(self):
        """Test that filter_data_by_country returns a DataFrame."""
        from src.dashboard import filter_data_by_country, DashboardState

        state = DashboardState()
        state.current_data = pd.DataFrame(
            {"location": ["UK", "Germany", "UK"], "value": [100, 200, 150]}
        )
        result = filter_data_by_country(state, ["UK"])
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2


class TestExportData:
    """Tests for export_data function."""

    def test_export_data_exists(self):
        """Test that export_data function is defined."""
        from src.dashboard import export_data

        assert export_data is not None

    def test_export_data_returns_result(self):
        """Test that export_data returns a result dictionary."""
        from src.dashboard import export_data, DashboardState
        import tempfile
        import os

        state = DashboardState()
        state.current_data = pd.DataFrame({"location": ["UK"], "value": [100]})

        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
            filepath = f.name

        try:
            result = export_data(state, filepath)
            assert isinstance(result, dict)
            assert "success" in result
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)
