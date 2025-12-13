"""
Tests for Dashboard Class (OOP)

Tests for the Dashboard class that encapsulates data loading,
state management, and provides a clean OOP interface.
"""

import pytest
import pandas as pd


@pytest.fixture
def sample_csv(tmp_path):
    """Create a sample CSV file for testing."""
    csv_content = """location,date,total_vaccinations,daily_vaccinations
Spain,2021-01-01,100,10
Spain,2021-06-01,200,20
Germany,2021-01-01,150,15
Germany,2021-06-01,250,25
France,2021-01-01,120,12
France,2021-06-01,220,22"""

    csv_file = tmp_path / "test_data.csv"
    csv_file.write_text(csv_content)
    return str(csv_file)


@pytest.fixture
def sample_dataframe():
    """Sample DataFrame for testing."""
    return pd.DataFrame(
        {
            "location": ["Spain", "Spain", "Germany", "Germany"],
            "date": pd.to_datetime(
                ["2021-01-01", "2021-06-01", "2021-01-01", "2021-06-01"]
            ),
            "total_vaccinations": [100, 200, 150, 250],
            "daily_vaccinations": [10, 20, 15, 25],
        }
    )


class TestDashboardClass:
    """Tests for Dashboard class existence and initialization."""

    def test_dashboard_class_exists(self):
        """Test that Dashboard class is defined."""
        from src.dashboard import Dashboard

        assert Dashboard is not None

    def test_dashboard_initialization(self):
        """Test that Dashboard can be instantiated."""
        from src.dashboard import Dashboard

        dashboard = Dashboard()
        assert dashboard is not None

    def test_dashboard_starts_empty(self):
        """Test that Dashboard starts with no data."""
        from src.dashboard import Dashboard

        dashboard = Dashboard()
        assert dashboard.data is None


class TestDashboardLoad:
    """Tests for load() method."""

    def test_load_method_exists(self):
        """Test that load method is defined."""
        from src.dashboard import Dashboard

        dashboard = Dashboard()
        assert hasattr(dashboard, "load")

    def test_load_returns_success_info(self, sample_csv):
        """Test that load returns success information."""
        from src.dashboard import Dashboard

        dashboard = Dashboard()
        result = dashboard.load(sample_csv)

        assert result["success"] is True
        assert "row_count" in result

    def test_load_populates_data(self, sample_csv):
        """Test that load populates the data."""
        from src.dashboard import Dashboard

        dashboard = Dashboard()
        dashboard.load(sample_csv)

        assert dashboard.data is not None
        assert len(dashboard.data) == 6


class TestDashboardProperties:
    """Tests for Dashboard properties."""

    def test_data_property_exists(self):
        """Test that data property is defined."""
        from src.dashboard import Dashboard

        dashboard = Dashboard()
        assert hasattr(dashboard, "data")

    def test_data_returns_copy(self, sample_csv):
        """Test that data returns copy (encapsulation)."""
        from src.dashboard import Dashboard

        dashboard = Dashboard()
        dashboard.load(sample_csv)

        data1 = dashboard.data
        data1["new_col"] = 1
        data2 = dashboard.data

        assert "new_col" not in data2.columns

    def test_row_count_property(self, sample_csv):
        """Test row_count property."""
        from src.dashboard import Dashboard

        dashboard = Dashboard()
        dashboard.load(sample_csv)

        assert dashboard.row_count == 6

    def test_row_count_zero_when_empty(self):
        """Test row_count is 0 when no data."""
        from src.dashboard import Dashboard

        dashboard = Dashboard()
        assert dashboard.row_count == 0

    def test_is_loaded_property(self, sample_csv):
        """Test is_loaded property."""
        from src.dashboard import Dashboard

        dashboard = Dashboard()
        assert dashboard.is_loaded is False

        dashboard.load(sample_csv)
        assert dashboard.is_loaded is True


class TestDashboardSummary:
    """Tests for summary() method."""

    def test_summary_method_exists(self):
        """Test that summary method is defined."""
        from src.dashboard import Dashboard

        dashboard = Dashboard()
        assert hasattr(dashboard, "summary")

    def test_summary_returns_dict(self, sample_csv):
        """Test that summary returns a dictionary."""
        from src.dashboard import Dashboard

        dashboard = Dashboard()
        dashboard.load(sample_csv)

        result = dashboard.summary()
        assert isinstance(result, dict)

    def test_summary_contains_row_count(self, sample_csv):
        """Test that summary contains row count."""
        from src.dashboard import Dashboard

        dashboard = Dashboard()
        dashboard.load(sample_csv)

        result = dashboard.summary()
        assert "row_count" in result
        assert result["row_count"] == 6


class TestDashboardFilter:
    """Tests for filter() method returning DataFilter."""

    def test_filter_method_exists(self):
        """Test that filter method is defined."""
        from src.dashboard import Dashboard

        dashboard = Dashboard()
        assert hasattr(dashboard, "filter")

    def test_filter_requires_db_connection(self, sample_csv):
        """Test that filter raises error without db_connection."""
        from src.dashboard import Dashboard

        dashboard = Dashboard()
        dashboard.load(sample_csv)

        # Without db_connection, should raise ValueError
        with pytest.raises(ValueError, match="No database connection"):
            dashboard.filter()

    def test_filter_returns_data_filter_with_db(self, sample_csv, tmp_path):
        """Test that filter returns DataFilter instance when db is set up."""
        from src.dashboard import Dashboard
        from src.filters import DataFilter
        from src.database import create_connection, insert_dataframe

        dashboard = Dashboard()
        dashboard.load(sample_csv)

        # Set up database connection
        db_path = str(tmp_path / "test.db")
        dashboard.db_connection = create_connection(db_path)
        insert_dataframe(dashboard.db_connection, "vaccinations", dashboard.data)

        result = dashboard.filter()
        assert isinstance(result, DataFilter)


class TestDashboardSetData:
    """Tests for set_data() method."""

    def test_set_data_method_exists(self):
        """Test that set_data method is defined."""
        from src.dashboard import Dashboard

        dashboard = Dashboard()
        assert hasattr(dashboard, "set_data")

    def test_set_data_updates_data(self, sample_dataframe):
        """Test that set_data updates internal data."""
        from src.dashboard import Dashboard

        dashboard = Dashboard()
        dashboard.set_data(sample_dataframe)

        assert dashboard.row_count == 4

    def test_set_data_makes_copy(self, sample_dataframe):
        """Test that set_data makes a copy."""
        from src.dashboard import Dashboard

        dashboard = Dashboard()
        dashboard.set_data(sample_dataframe)

        # Modify original
        sample_dataframe["new_col"] = 1

        # Dashboard should not have new column
        assert "new_col" not in dashboard.data.columns
