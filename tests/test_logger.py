"""
Tests for Activity Logger Module

Tests for logging user activities and actions in the dashboard.
"""

import pytest
import os
import tempfile
from datetime import datetime


class TestLogActivity:
    """Tests for log_activity function."""

    def test_log_activity_exists(self):
        """Test that log_activity function is defined."""
        from src.logger import log_activity

        assert log_activity is not None

    def test_log_activity_creates_log_entry(self):
        """Test that log_activity creates a log entry."""
        from src.logger import log_activity, get_log_entries

        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = os.path.join(tmpdir, "test.log")
            log_activity("test_action", "Test details", log_file=log_file)

            entries = get_log_entries(log_file)
            assert len(entries) >= 1

    def test_log_activity_includes_timestamp(self):
        """Test that log entries include timestamp."""
        from src.logger import log_activity, get_log_entries

        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = os.path.join(tmpdir, "test.log")
            log_activity("test_action", "Test details", log_file=log_file)

            entries = get_log_entries(log_file)
            assert "timestamp" in entries[-1] or any(
                char.isdigit() for char in str(entries[-1])
            )

    def test_log_activity_includes_action(self):
        """Test that log entries include action name."""
        from src.logger import log_activity, get_log_entries

        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = os.path.join(tmpdir, "test.log")
            log_activity("LOAD_DATA", "Loaded vaccinations.csv", log_file=log_file)

            entries = get_log_entries(log_file)
            assert "LOAD_DATA" in str(entries[-1])


class TestGetLogEntries:
    """Tests for get_log_entries function."""

    def test_get_log_entries_exists(self):
        """Test that get_log_entries function is defined."""
        from src.logger import get_log_entries

        assert get_log_entries is not None

    def test_get_log_entries_returns_list(self):
        """Test that get_log_entries returns a list."""
        from src.logger import get_log_entries

        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = os.path.join(tmpdir, "test.log")
            # Create empty log file
            open(log_file, "w").close()

            entries = get_log_entries(log_file)
            assert isinstance(entries, list)

    def test_get_log_entries_handles_missing_file(self):
        """Test that get_log_entries handles missing file gracefully."""
        from src.logger import get_log_entries

        entries = get_log_entries("/nonexistent/path/log.txt")
        assert entries == []


class TestClearLog:
    """Tests for clear_log function."""

    def test_clear_log_exists(self):
        """Test that clear_log function is defined."""
        from src.logger import clear_log

        assert clear_log is not None

    def test_clear_log_removes_entries(self):
        """Test that clear_log removes all entries."""
        from src.logger import log_activity, clear_log, get_log_entries

        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = os.path.join(tmpdir, "test.log")
            log_activity("test", "details", log_file=log_file)
            clear_log(log_file)

            entries = get_log_entries(log_file)
            assert len(entries) == 0


class TestGetSessionLog:
    """Tests for get_session_log function."""

    def test_get_session_log_exists(self):
        """Test that get_session_log function is defined."""
        from src.logger import get_session_log

        assert get_session_log is not None

    def test_get_session_log_returns_list(self):
        """Test that get_session_log returns a list."""
        from src.logger import get_session_log

        log = get_session_log()
        assert isinstance(log, list)


class TestLoggerIntegration:
    """Integration tests for logger module."""

    def test_multiple_logs(self):
        """Test logging multiple activities."""
        from src.logger import log_activity, get_log_entries

        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = os.path.join(tmpdir, "test.log")

            log_activity("LOAD_DATA", "Loaded data", log_file=log_file)
            log_activity("FILTER", "Filtered by country", log_file=log_file)
            log_activity("EXPORT", "Exported to CSV", log_file=log_file)

            entries = get_log_entries(log_file)
            assert len(entries) >= 3

    def test_log_format(self):
        """Test that log entries have proper format."""
        from src.logger import log_activity, get_log_entries

        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = os.path.join(tmpdir, "test.log")
            log_activity("TEST_ACTION", "Test details here", log_file=log_file)

            entries = get_log_entries(log_file)
            entry = entries[-1]

            # Should contain action and details
            assert "TEST_ACTION" in str(entry)
            assert "Test details" in str(entry)
