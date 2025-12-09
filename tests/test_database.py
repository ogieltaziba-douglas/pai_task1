"""
Test module for database.py

Tests cover:
- SQLite database connection management
- Table creation with schema definition
- Data insertion from DataFrames
- Data retrieval and querying
- CRUD operations (Create, Read, Update, Delete)
- Error handling and edge cases
"""

import pytest
import pandas as pd
import sqlite3
import os
import tempfile

from src.database import (
    create_connection,
    close_connection,
    create_table,
    insert_dataframe,
    fetch_all,
    execute_query,
    create_record,
    read_record,
    update_record,
    delete_record,
    table_exists,
)


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def temp_db():
    """Create a temporary database file."""
    fd, filepath = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    yield filepath
    if os.path.exists(filepath):
        os.unlink(filepath)


@pytest.fixture
def sample_dataframe():
    """Create a sample DataFrame for testing."""
    return pd.DataFrame(
        {
            "location": ["United Kingdom", "United States", "Germany"],
            "iso_code": ["GBR", "USA", "DEU"],
            "date": ["2021-01-01", "2021-01-01", "2021-01-02"],
            "total_vaccinations": [1000000, 5000000, 500000],
            "people_vaccinated": [800000, 4000000, 400000],
        }
    )


@pytest.fixture
def connected_db(temp_db):
    """Provide a connected database for testing."""
    conn = create_connection(temp_db)
    yield conn
    close_connection(conn)


# ============================================================================
# Tests for Connection Management
# ============================================================================


class TestConnectionManagement:
    """Test database connection functions."""

    def test_create_connection_returns_connection(self, temp_db):
        """Test that create_connection returns a sqlite3 Connection."""
        conn = create_connection(temp_db)
        assert isinstance(conn, sqlite3.Connection)
        close_connection(conn)

    def test_create_connection_creates_file(self, temp_db):
        """Test that connection creates the database file."""
        conn = create_connection(temp_db)
        assert os.path.exists(temp_db)
        close_connection(conn)

    def test_create_connection_in_memory(self):
        """Test creating an in-memory database."""
        conn = create_connection(":memory:")
        assert isinstance(conn, sqlite3.Connection)
        close_connection(conn)

    def test_close_connection_success(self, temp_db):
        """Test that close_connection properly closes the connection."""
        conn = create_connection(temp_db)
        result = close_connection(conn)
        assert result is True


# ============================================================================
# Tests for Table Operations
# ============================================================================


class TestTableOperations:
    """Test table creation and management."""

    def test_create_table_success(self, connected_db):
        """Test creating a table with specified columns."""
        columns = {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "location": "TEXT",
            "iso_code": "TEXT",
            "total_vaccinations": "INTEGER",
        }
        result = create_table(connected_db, "vaccinations", columns)
        assert result is True

    def test_create_table_adds_to_database(self, connected_db):
        """Test that created table exists in database."""
        columns = {"id": "INTEGER PRIMARY KEY", "name": "TEXT"}
        create_table(connected_db, "test_table", columns)
        assert table_exists(connected_db, "test_table") is True

    def test_table_exists_returns_false_for_nonexistent(self, connected_db):
        """Test table_exists returns False for non-existent table."""
        assert table_exists(connected_db, "nonexistent_table") is False


# ============================================================================
# Tests for Data Insertion
# ============================================================================


class TestDataInsertion:
    """Test data insertion functions."""

    def test_insert_dataframe_success(self, connected_db, sample_dataframe):
        """Test inserting a DataFrame into a table."""
        rows_inserted = insert_dataframe(connected_db, "vaccinations", sample_dataframe)
        assert rows_inserted == 3

    def test_insert_dataframe_creates_table(self, connected_db, sample_dataframe):
        """Test that insert_dataframe creates table if not exists."""
        insert_dataframe(connected_db, "new_table", sample_dataframe)
        assert table_exists(connected_db, "new_table") is True

    def test_insert_empty_dataframe(self, connected_db):
        """Test inserting an empty DataFrame."""
        empty_df = pd.DataFrame()
        rows_inserted = insert_dataframe(connected_db, "empty_table", empty_df)
        assert rows_inserted == 0


# ============================================================================
# Tests for Data Retrieval
# ============================================================================


class TestDataRetrieval:
    """Test data retrieval functions."""

    def test_fetch_all_returns_dataframe(self, connected_db, sample_dataframe):
        """Test that fetch_all returns a DataFrame."""
        insert_dataframe(connected_db, "vaccinations", sample_dataframe)
        result = fetch_all(connected_db, "vaccinations")
        assert isinstance(result, pd.DataFrame)

    def test_fetch_all_correct_data(self, connected_db, sample_dataframe):
        """Test that fetched data matches inserted data."""
        insert_dataframe(connected_db, "vaccinations", sample_dataframe)
        result = fetch_all(connected_db, "vaccinations")
        assert len(result) == 3
        assert "United Kingdom" in result["location"].values

    def test_fetch_all_empty_table(self, connected_db):
        """Test fetching from an empty table."""
        columns = {"id": "INTEGER PRIMARY KEY", "name": "TEXT"}
        create_table(connected_db, "empty_table", columns)
        result = fetch_all(connected_db, "empty_table")
        assert len(result) == 0

    def test_execute_query_select(self, connected_db, sample_dataframe):
        """Test executing a custom SELECT query."""
        insert_dataframe(connected_db, "vaccinations", sample_dataframe)
        query = "SELECT location, total_vaccinations FROM vaccinations WHERE iso_code = 'GBR'"
        result = execute_query(connected_db, query)
        assert len(result) == 1
        assert result.iloc[0]["location"] == "United Kingdom"


# ============================================================================
# Tests for CRUD Operations
# ============================================================================


class TestCRUDOperations:
    """Test Create, Read, Update, Delete operations."""

    def test_create_record_success(self, connected_db, sample_dataframe):
        """Test creating a single record."""
        insert_dataframe(connected_db, "vaccinations", sample_dataframe)
        new_record = {
            "location": "France",
            "iso_code": "FRA",
            "date": "2021-01-03",
            "total_vaccinations": 750000,
            "people_vaccinated": 600000,
        }
        record_id = create_record(connected_db, "vaccinations", new_record)
        assert record_id is not None

    def test_read_record_by_id(self, connected_db, sample_dataframe):
        """Test reading a record by its ID."""
        insert_dataframe(connected_db, "vaccinations", sample_dataframe)
        # Read the first record (rowid 1)
        result = read_record(connected_db, "vaccinations", 1)
        assert result is not None
        assert result["location"] == "United Kingdom"

    def test_read_record_not_found(self, connected_db, sample_dataframe):
        """Test reading a non-existent record returns None."""
        insert_dataframe(connected_db, "vaccinations", sample_dataframe)
        result = read_record(connected_db, "vaccinations", 999)
        assert result is None

    def test_update_record_success(self, connected_db, sample_dataframe):
        """Test updating a record."""
        insert_dataframe(connected_db, "vaccinations", sample_dataframe)
        updates = {"total_vaccinations": 1500000}
        result = update_record(connected_db, "vaccinations", 1, updates)
        assert result is True

        # Verify the update
        record = read_record(connected_db, "vaccinations", 1)
        assert record["total_vaccinations"] == 1500000

    def test_delete_record_success(self, connected_db, sample_dataframe):
        """Test deleting a record."""
        insert_dataframe(connected_db, "vaccinations", sample_dataframe)
        result = delete_record(connected_db, "vaccinations", 1)
        assert result is True

        # Verify deletion
        record = read_record(connected_db, "vaccinations", 1)
        assert record is None

    def test_delete_nonexistent_record(self, connected_db, sample_dataframe):
        """Test deleting a non-existent record returns False."""
        insert_dataframe(connected_db, "vaccinations", sample_dataframe)
        result = delete_record(connected_db, "vaccinations", 999)
        assert result is False


# ============================================================================
# Integration Tests
# ============================================================================


class TestDatabaseIntegration:
    """Integration tests for database operations."""

    def test_full_workflow(self, temp_db, sample_dataframe):
        """Test complete database workflow."""
        # Connect
        conn = create_connection(temp_db)

        # Insert data
        insert_dataframe(conn, "vaccinations", sample_dataframe)

        # Read all
        all_data = fetch_all(conn, "vaccinations")
        assert len(all_data) == 3

        # Create new record
        new_record = {
            "location": "Canada",
            "iso_code": "CAN",
            "date": "2021-01-05",
            "total_vaccinations": 300000,
            "people_vaccinated": 250000,
        }
        create_record(conn, "vaccinations", new_record)

        # Verify count increased
        all_data = fetch_all(conn, "vaccinations")
        assert len(all_data) == 4

        # Close
        close_connection(conn)
