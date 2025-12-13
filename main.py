#!/usr/bin/env python3
"""
Public Health Data Insights Dashboard

Main entry point for the application.
This tool allows researchers to analyse public health vaccination data.

Usage:
    python main.py
"""

import os
import sys

# Add src to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.dashboard import DashboardState
from src.cli import get_user_input
from src.menu_handlers import (
    handle_load_data,
    handle_view_summary,
    handle_filter_country,
    handle_filter_continent,
    handle_filter_income,
    handle_filter_date,
    handle_statistics,
    handle_trends,
    handle_charts,
    handle_export,
)


def display_menu():
    """Display the main menu."""
    print("\n" + "=" * 50)
    print("  Public Health Data Insights Dashboard")
    print("=" * 50)
    print("  1.  Load data from CSV")
    print("  2.  View data summary")
    print("  ─── FILTERS ───────────")
    print("  3.  Filter by country")
    print("  4.  Filter by continent")
    print("  5.  Filter by income group")
    print("  6.  Filter by date range")
    print("  ─── ANALYSIS ──────────")
    print("  7.  View statistics")
    print("  8.  View trends")
    print("  9.  Generate charts")
    print("  ─── EXPORT ────────────")
    print("  10. Export data to CSV")
    print("  ─────────────────────")
    print("  0.  Exit")
    print("=" * 50)


def main():
    """Main entry point."""
    print("\n" + "=" * 60)
    print("  Welcome to the Public Health Data Insights Dashboard")
    print("=" * 60)
    print("\nThis tool helps researchers analyse COVID-19 vaccination data.")

    state = DashboardState()

    handlers = {
        "1": handle_load_data,
        "2": handle_view_summary,
        "3": handle_filter_country,
        "4": handle_filter_continent,
        "5": handle_filter_income,
        "6": handle_filter_date,
        "7": handle_statistics,
        "8": handle_trends,
        "9": handle_charts,
        "10": handle_export,
    }

    while True:
        display_menu()
        choice = get_user_input("Enter your choice")

        if choice == "0":
            print("\nThank you for using the Dashboard! Goodbye!\n")
            break

        handler = handlers.get(choice)
        if handler:
            handler(state)
        else:
            print("\n✗ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
