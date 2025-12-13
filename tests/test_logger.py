"""
Tests for Activity Logger Module (OOP-Only)

Tests for the ActivityLogger class that provides activity logging
with proper encapsulation and OOP principles.
"""

import pytest
import os
import tempfile


class TestActivityLoggerClass:
    """Tests for ActivityLogger class existence and initialization."""

    def test_activity_logger_class_exists(self):
        """Test that ActivityLogger class is defined."""
        from src.logger import ActivityLogger

        assert ActivityLogger is not None

    def test_activity_logger_initialization_default(self):
        """Test that ActivityLogger can be instantiated with defaults."""
        from src.logger import ActivityLogger

        logger = ActivityLogger()
        assert logger is not None

    def test_activity_logger_initialization_custom_file(self):
        """Test that ActivityLogger accepts custom log file."""
        from src.logger import ActivityLogger

        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = os.path.join(tmpdir, "custom.log")
            logger = ActivityLogger(log_file=log_file)
            assert logger is not None


class TestActivityLoggerLogMethod:
    """Tests for the log() method."""

    def test_log_method_exists(self):
        """Test that log method is defined."""
        from src.logger import ActivityLogger

        logger = ActivityLogger()
        assert hasattr(logger, "log")

    def test_log_creates_session_entry(self):
        """Test that log() adds entry to session."""
        from src.logger import ActivityLogger

        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = os.path.join(tmpdir, "test.log")
            logger = ActivityLogger(log_file=log_file)
            logger.log("TEST", "Test details")

            assert len(logger.session_entries) == 1

    def test_log_creates_file_entry(self):
        """Test that log() writes to file."""
        from src.logger import ActivityLogger

        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = os.path.join(tmpdir, "test.log")
            logger = ActivityLogger(log_file=log_file)
            logger.log("TEST", "Test details")

            assert len(logger.file_entries) >= 1

    def test_log_includes_timestamp(self):
        """Test that log entries include timestamp."""
        from src.logger import ActivityLogger

        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = os.path.join(tmpdir, "test.log")
            logger = ActivityLogger(log_file=log_file)
            logger.log("TEST", "Test details")

            entry = logger.session_entries[0]
            assert "[" in entry and "]" in entry  # timestamp brackets

    def test_log_includes_action(self):
        """Test that log entries include action name."""
        from src.logger import ActivityLogger

        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = os.path.join(tmpdir, "test.log")
            logger = ActivityLogger(log_file=log_file)
            logger.log("LOAD_DATA", "Loaded file")

            entry = logger.session_entries[0]
            assert "LOAD_DATA" in entry


class TestActivityLoggerProperties:
    """Tests for properties (encapsulation)."""

    def test_session_entries_property_exists(self):
        """Test that session_entries property is defined."""
        from src.logger import ActivityLogger

        logger = ActivityLogger()
        assert hasattr(logger, "session_entries")

    def test_session_entries_returns_list(self):
        """Test that session_entries returns a list."""
        from src.logger import ActivityLogger

        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = os.path.join(tmpdir, "test.log")
            logger = ActivityLogger(log_file=log_file)

            assert isinstance(logger.session_entries, list)

    def test_session_entries_returns_copy(self):
        """Test that session_entries returns copy (encapsulation)."""
        from src.logger import ActivityLogger

        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = os.path.join(tmpdir, "test.log")
            logger = ActivityLogger(log_file=log_file)

            entries = logger.session_entries
            entries.append("FAKE ENTRY")

            assert "FAKE ENTRY" not in logger.session_entries

    def test_file_entries_property_exists(self):
        """Test that file_entries property is defined."""
        from src.logger import ActivityLogger

        logger = ActivityLogger()
        assert hasattr(logger, "file_entries")

    def test_file_entries_returns_list(self):
        """Test that file_entries returns a list."""
        from src.logger import ActivityLogger

        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = os.path.join(tmpdir, "test.log")
            logger = ActivityLogger(log_file=log_file)

            assert isinstance(logger.file_entries, list)


class TestActivityLoggerClear:
    """Tests for clear() method."""

    def test_clear_method_exists(self):
        """Test that clear method is defined."""
        from src.logger import ActivityLogger

        logger = ActivityLogger()
        assert hasattr(logger, "clear")

    def test_clear_removes_session_entries(self):
        """Test that clear() removes session entries."""
        from src.logger import ActivityLogger

        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = os.path.join(tmpdir, "test.log")
            logger = ActivityLogger(log_file=log_file)
            logger.log("TEST", "details")
            logger.clear()

            assert len(logger.session_entries) == 0

    def test_clear_removes_file_entries(self):
        """Test that clear() removes file entries."""
        from src.logger import ActivityLogger

        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = os.path.join(tmpdir, "test.log")
            logger = ActivityLogger(log_file=log_file)
            logger.log("TEST", "details")
            logger.clear()

            assert len(logger.file_entries) == 0


class TestActivityLoggerIntegration:
    """Integration tests for ActivityLogger."""

    def test_multiple_logs(self):
        """Test logging multiple activities."""
        from src.logger import ActivityLogger

        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = os.path.join(tmpdir, "test.log")
            logger = ActivityLogger(log_file=log_file)

            logger.log("LOAD_DATA", "Loaded data")
            logger.log("FILTER", "Filtered by country")
            logger.log("EXPORT", "Exported to CSV")

            assert len(logger.session_entries) == 3
            assert len(logger.file_entries) == 3

    def test_log_format(self):
        """Test that log entries have proper format."""
        from src.logger import ActivityLogger

        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = os.path.join(tmpdir, "test.log")
            logger = ActivityLogger(log_file=log_file)
            logger.log("TEST_ACTION", "Test details here")

            entry = logger.session_entries[0]

            assert "TEST_ACTION" in entry
            assert "Test details" in entry
