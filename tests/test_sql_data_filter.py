"""
Tests for SQLDataFilter Class

Tests for the SQLDataFilter class that provides SQL-based filtering
with method chaining, demonstrating LO3 SQL skills.
"""

import pytest
import pandas as pd
import sqlite3


@pytest.fixture
def test_db():
    """Create in-memory SQLite database with test data."""
    conn = sqlite3.connect(":memory:")

    # Create test data
    data = pd.DataFrame(
        {
            "location": ["Spain", "Spain", "Germany", "Germany", "France", "France"],
            "date": [
                "2021-01-01",
                "2021-06-01",
                "2021-01-01",
                "2021-06-01",
                "2021-01-01",
                "2021-06-01",
            ],
            "total_vaccinations": [100, 200, 150, 250, 120, 220],
            "continent": ["Europe", "Europe", "Europe", "Europe", "Europe", "Europe"],
        }
    )

    data.to_sql("vaccinations", conn, index=False, if_exists="replace")

    yield conn
    conn.close()


class TestSQLDataFilterClass:
    """Tests for SQLDataFilter class existence and initialization."""

    def test_sql_data_filter_class_exists(self):
        """Test that SQLDataFilter class is defined."""
        from src.database import SQLDataFilter

        assert SQLDataFilter is not None

    def test_sql_data_filter_initialization(self, test_db):
        """Test that SQLDataFilter can be instantiated."""
        from src.database import SQLDataFilter

        df = SQLDataFilter(test_db)
        assert df is not None

    def test_sql_data_filter_accepts_table_name(self, test_db):
        """Test that SQLDataFilter accepts custom table name."""
        from src.database import SQLDataFilter

        df = SQLDataFilter(test_db, table="vaccinations")
        assert df is not None


class TestSQLDataFilterByCountry:
    """Tests for by_country() method with SQL."""

    def test_by_country_method_exists(self, test_db):
        """Test that by_country method is defined."""
        from src.database import SQLDataFilter

        df = SQLDataFilter(test_db)
        assert hasattr(df, "by_country")

    def test_by_country_returns_sql_data_filter(self, test_db):
        """Test that by_country returns SQLDataFilter for chaining."""
        from src.database import SQLDataFilter

        df = SQLDataFilter(test_db)
        result = df.by_country("Spain")

        assert isinstance(result, SQLDataFilter)

    def test_by_country_filters_correctly(self, test_db):
        """Test that by_country generates correct SQL."""
        from src.database import SQLDataFilter

        df = SQLDataFilter(test_db)
        result = df.by_country("Spain").result()

        assert len(result) == 2
        assert all(result["location"] == "Spain")

    def test_by_country_multiple_countries(self, test_db):
        """Test filtering by multiple countries."""
        from src.database import SQLDataFilter

        df = SQLDataFilter(test_db)
        result = df.by_country(["Spain", "Germany"]).result()

        assert len(result) == 4


class TestSQLDataFilterByDateRange:
    """Tests for by_date_range() method with SQL."""

    def test_by_date_range_method_exists(self, test_db):
        """Test that by_date_range method is defined."""
        from src.database import SQLDataFilter

        df = SQLDataFilter(test_db)
        assert hasattr(df, "by_date_range")

    def test_by_date_range_returns_sql_data_filter(self, test_db):
        """Test that by_date_range returns SQLDataFilter for chaining."""
        from src.database import SQLDataFilter

        df = SQLDataFilter(test_db)
        result = df.by_date_range(start="2021-01-01")

        assert isinstance(result, SQLDataFilter)

    def test_by_date_range_filters_start(self, test_db):
        """Test filtering with start date only."""
        from src.database import SQLDataFilter

        df = SQLDataFilter(test_db)
        result = df.by_date_range(start="2021-03-01").result()

        assert len(result) == 3  # Only June dates

    def test_by_date_range_filters_end(self, test_db):
        """Test filtering with end date only."""
        from src.database import SQLDataFilter

        df = SQLDataFilter(test_db)
        result = df.by_date_range(end="2021-03-01").result()

        assert len(result) == 3  # Only January dates


class TestSQLDataFilterResult:
    """Tests for result() method."""

    def test_result_method_exists(self, test_db):
        """Test that result method is defined."""
        from src.database import SQLDataFilter

        df = SQLDataFilter(test_db)
        assert hasattr(df, "result")

    def test_result_returns_dataframe(self, test_db):
        """Test that result returns a DataFrame."""
        from src.database import SQLDataFilter

        df = SQLDataFilter(test_db)
        result = df.result()

        assert isinstance(result, pd.DataFrame)

    def test_result_returns_all_rows_without_filter(self, test_db):
        """Test that result returns all rows when no filters."""
        from src.database import SQLDataFilter

        df = SQLDataFilter(test_db)
        result = df.result()

        assert len(result) == 6


class TestSQLDataFilterChaining:
    """Tests for method chaining with SQL."""

    def test_chain_country_then_date(self, test_db):
        """Test chaining country and date filters."""
        from src.database import SQLDataFilter

        result = (
            SQLDataFilter(test_db)
            .by_country("Spain")
            .by_date_range(start="2021-03-01")
            .result()
        )

        assert len(result) == 1
        assert result.iloc[0]["location"] == "Spain"

    def test_chain_date_then_country(self, test_db):
        """Test chaining date then country filters."""
        from src.database import SQLDataFilter

        result = (
            SQLDataFilter(test_db)
            .by_date_range(end="2021-03-01")
            .by_country("Germany")
            .result()
        )

        assert len(result) == 1
        assert result.iloc[0]["location"] == "Germany"


class TestSQLDataFilterQuery:
    """Tests for SQL query generation."""

    def test_query_property_exists(self, test_db):
        """Test that query property is defined."""
        from src.database import SQLDataFilter

        df = SQLDataFilter(test_db)
        assert hasattr(df, "query")

    def test_query_returns_string(self, test_db):
        """Test that query returns SQL string."""
        from src.database import SQLDataFilter

        df = SQLDataFilter(test_db)
        assert isinstance(df.query, str)

    def test_query_contains_select(self, test_db):
        """Test that query contains SELECT."""
        from src.database import SQLDataFilter

        df = SQLDataFilter(test_db)
        assert "SELECT" in df.query.upper()

    def test_query_contains_where_after_filter(self, test_db):
        """Test that query contains WHERE after filtering."""
        from src.database import SQLDataFilter

        df = SQLDataFilter(test_db).by_country("Spain")
        assert "WHERE" in df.query.upper()


class TestSQLDataFilterCount:
    """Tests for count property."""

    def test_count_property_exists(self, test_db):
        """Test that count property is defined."""
        from src.database import SQLDataFilter

        df = SQLDataFilter(test_db)
        assert hasattr(df, "count")

    def test_count_returns_integer(self, test_db):
        """Test that count returns integer."""
        from src.database import SQLDataFilter

        df = SQLDataFilter(test_db)
        assert isinstance(df.count, int)
        assert df.count == 6

    def test_count_after_filter(self, test_db):
        """Test count after filtering."""
        from src.database import SQLDataFilter

        df = SQLDataFilter(test_db).by_country("Spain")
        assert df.count == 2
