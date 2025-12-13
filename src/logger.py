"""
Activity Logger Module (OOP-Only)

Provides the ActivityLogger class for tracking user activities
in the Public Health Data Insights Dashboard.

OOP Principles Demonstrated:
- Encapsulation: Private attributes with property accessors
- Methods: Behavior encapsulated in class methods
- Single Responsibility: One class, one purpose

Usage:
    from src.logger import ActivityLogger

    logger = ActivityLogger()
    logger.log('LOAD_DATA', 'Loaded 196,246 records')
    print(logger.session_entries)
"""

from typing import List


class ActivityLogger:
    """
    Activity Logger for tracking user actions.

    Attributes:
        _session_log (List[str]): Private session log entries
        _log_file (str): Path to log file

    Example:
        >>> logger = ActivityLogger()
        >>> logger.log('LOAD_DATA', 'Loaded data')
        >>> print(logger.session_entries)
        ['[2025-12-13 18:00:00] LOAD_DATA: Loaded data']
    """

    def __init__(self, log_file: str = "logs/activity.log"):
        """
        Initialize the ActivityLogger.

        Args:
            log_file: Path to log file (default: logs/activity.log)
        """
        raise NotImplementedError("ActivityLogger.__init__ not implemented")

    def log(self, action: str, details: str) -> None:
        """
        Log an activity.

        Args:
            action: Action name (e.g., 'LOAD_DATA', 'FILTER')
            details: Description of the activity
        """
        raise NotImplementedError("ActivityLogger.log not implemented")

    @property
    def session_entries(self) -> List[str]:
        """
        Get session log entries (returns copy for encapsulation).

        Returns:
            Copy of session log entries
        """
        raise NotImplementedError("ActivityLogger.session_entries not implemented")

    @property
    def file_entries(self) -> List[str]:
        """
        Get log entries from file.

        Returns:
            List of log entries from file
        """
        raise NotImplementedError("ActivityLogger.file_entries not implemented")

    def clear(self) -> None:
        """Clear all log entries (session and file)."""
        raise NotImplementedError("ActivityLogger.clear not implemented")
