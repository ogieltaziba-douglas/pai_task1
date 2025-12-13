"""
Tests for Dashboard Module

Tests for business logic and data operations.
"""

import pandas as pd
from unittest.mock import patch


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

    def test_get_trend_analysis_has_direction(self, tmp_path):
        """Test that trend analysis includes direction."""
        from src.dashboard import get_trend_analysis, DashboardState
        from src.database import create_connection, insert_dataframe

        state = DashboardState()
        state.current_data = pd.DataFrame(
            {
                "location": ["UK", "UK", "UK"],
                "date": pd.to_datetime(["2021-01-01", "2021-01-02", "2021-01-03"]),
                "daily_vaccinations": [100, 200, 300],
            }
        )
        # Set up database connection
        db_path = str(tmp_path / "test.db")
        state.db_connection = create_connection(db_path)
        insert_dataframe(state.db_connection, "vaccinations", state.current_data)

        result = get_trend_analysis(state, "UK")
        assert "direction" in result
