"""
Menu Handlers Module

This module contains all menu handler functions for processing
user interactions in the Public Health Data Insights Dashboard.

Functions:
    handle_load_data: Load data from CSV
    handle_view_summary: Display data summary
    handle_filter_country: Filter by country
    handle_filter_continent: Filter by continent
    handle_filter_income: Compare income groups
    handle_filter_date: Filter by date range
    handle_statistics: Display statistics
    handle_trends: Display trend analysis
    handle_charts: Generate charts
    handle_export: Export data to CSV
    display_country_menu: Display country selection menu
    display_column_menu: Display column selection menu
    format_preview: Format DataFrame preview
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

from src.dashboard import (
    DashboardState,
    load_data,
    get_summary,
    get_statistics,
    get_trend_analysis,
    filter_data_by_country,
    filter_data_by_continent,
    export_data,
    get_countries_only,
)
from src.constants import (
    CONTINENTS,
    INCOME_GROUPS,
    KEY_COUNTRIES,
    COLUMN_DESCRIPTIONS,
)
from src.filters import filter_by_country
from src.summaries import count_by_category
from src.visualizations import create_line_chart, display_table, save_chart
from src.cli import get_user_input
from src.database import create_connection, insert_dataframe, close_connection


def format_preview(df, note_missing=True):
    """Format DataFrame preview with user-friendly missing value display."""
    # Replace NaN with dash for display
    display_df = df.fillna("-")
    table = display_table(display_df)

    if note_missing and df.isna().any().any():
        missing_count = df.isna().sum().sum()
        table += (
            f"\n  Note: '-' indicates unreported data ({missing_count} missing values)"
        )

    return table


def display_country_menu():
    """Display key countries menu and return selected country."""
    print("\n" + "=" * 55)
    print("  Select a Country")
    print("=" * 55)

    country_list = []
    for continent, countries in KEY_COUNTRIES.items():
        print(f"\n  {continent}:")
        for country in countries:
            country_list.append(country)
            print(f"    {len(country_list):2}. {country}")

    print("\n" + "=" * 55)

    choice = get_user_input("Enter number or country name")

    if not choice:
        return None

    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(country_list):
            return country_list[idx]
        return None

    return choice.strip()


def display_column_menu(columns):
    """Display numbered column menu and return selected column."""
    print("\nSelect a column for statistics:")
    for i, col in enumerate(columns, 1):
        print(f"  {i:2}. {col}")

    choice = get_user_input("Enter number or column name")

    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(columns):
            return columns[idx]
        return None

    return choice.strip() if choice else "total_vaccinations"


def handle_load_data(state):
    """Handle data loading."""
    filepath = "data/vaccinations.csv"
    print(f"\nLoading data from {filepath}...")

    result = load_data(state, filepath)

    if result["success"]:
        print(
            f"\n✓ Loaded {result['row_count']:,} records with {result['column_count']} columns"
        )
        print(f"  Columns: {', '.join(result['columns'][:5])}...")

        # Inform user about missing value handling
        if result.get("missing_filled", 0) > 0:
            print("\n  Data Cleaning Applied:")
            print(
                f"    • {result['missing_filled']:,} missing values filled (forward fill)"
            )
            if result.get("missing_remaining", 0) > 0:
                print(
                    f"    • {result['missing_remaining']:,} values still missing (start of series)"
                )

        load_to_db = get_user_input("Load data into database? (y/n)").lower()
        if load_to_db == "y":
            try:
                db_conn = create_connection("data/vaccinations.db")
                rows = insert_dataframe(db_conn, "vaccinations", state.current_data)
                print(f"\n✓ Inserted {rows:,} records into database")
                close_connection(db_conn)
            except Exception as e:
                print(f"\n✗ Error: {e}")
    else:
        print(f"\n✗ Error: {result['error']}")


def handle_view_summary(state):
    """Handle summary view."""
    if state.current_data is None:
        print("\n✗ No data loaded. Please load data first (Option 1).")
        return

    summary = get_summary(state)

    print("\n" + "=" * 40)
    print("Data Summary")
    print("=" * 40)
    print(f"  Total Records: {summary['total_records']:,}")
    if summary.get("date_range"):
        print("  Date Range:")
        print(f"    Min: {summary['date_range']['min']}")
        print(f"    Max: {summary['date_range']['max']}")
    if summary.get("unique_locations"):
        print(f"  Unique Locations: {summary['unique_locations']}")
    print("=" * 40)

    # Show top countries
    countries_only = get_countries_only(state.current_data)
    print("\nRecords by Country (Top 10):")
    country_counts = count_by_category(countries_only, "location")
    print(country_counts.head(10).to_string())


def handle_filter_country(state):
    """Handle country filter."""
    if state.current_data is None:
        print("\n✗ No data loaded. Please load data first (Option 1).")
        return

    country = display_country_menu()
    if not country:
        print("\n✗ No selection entered.")
        return

    filtered = filter_data_by_country(state, [country])

    if filtered.empty:
        print(f"\n✗ No data found for: {country}")
        return

    print(f"\n✓ Filtered to {len(filtered):,} records for: {country}")

    print("\nPreview (first 10 rows):")
    cols = ["location", "date", "total_vaccinations", "daily_vaccinations"]
    available = [c for c in cols if c in filtered.columns]
    preview = filtered[available].head(10).reset_index(drop=True)
    print(format_preview(preview))

    if get_user_input("Use filtered data? (y/n)").lower() == "y":
        state.current_data = filtered
        print("✓ Now using filtered data.")


def handle_filter_continent(state):
    """Handle continent filter."""
    print("\nNote: This will reload fresh data from the original CSV.")

    print("\nAvailable continents:")
    for i, c in enumerate(CONTINENTS, 1):
        print(f"  {i}. {c}")

    choice = get_user_input("Enter number or continent name")

    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(CONTINENTS):
            continent = CONTINENTS[idx]
        else:
            print("\n✗ Invalid selection.")
            return
    else:
        continent = choice.strip() if choice else None

    if not continent:
        print("\n✗ No selection entered.")
        return

    filtered = filter_data_by_continent(continent)

    if filtered.empty:
        print(f"\n✗ No data found for: {continent}")
        return

    print(f"\n✓ Filtered to {len(filtered):,} records for: {continent}")

    print("\nPreview (first 10 rows):")
    cols = ["location", "date", "total_vaccinations", "daily_vaccinations"]
    available = [c for c in cols if c in filtered.columns]
    preview = filtered[available].head(10).reset_index(drop=True)
    print(format_preview(preview))

    if get_user_input("Use this data? (y/n)").lower() == "y":
        state.current_data = filtered
        print("✓ Now using continent data.")


def handle_filter_income(state):
    """Handle income group comparison."""
    print("\n" + "=" * 60)
    print("  Income Group Vaccination Comparison")
    print("=" * 60)

    from src.data_loader import load_csv
    from src.data_cleaner import convert_dates

    try:
        fresh_data = load_csv("data/vaccinations.csv")
        fresh_data = convert_dates(fresh_data, ["date"], errors="coerce")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return

    print("\nComparing latest vaccination rates across income groups...\n")

    print(f"{'Income Group':<25} {'Total Vaccinations':>20} {'Per 100 People':>15}")
    print("-" * 62)

    for group in INCOME_GROUPS:
        group_data = filter_by_country(fresh_data, [group])
        if not group_data.empty:
            latest = group_data.sort_values("date").iloc[-1]
            total = latest.get("total_vaccinations", 0)
            per_100 = latest.get("total_vaccinations_per_hundred", 0)

            total_str = f"{total:,.0f}" if pd.notna(total) else "N/A"
            per_100_str = f"{per_100:.1f}" if pd.notna(per_100) else "N/A"

            print(f"{group:<25} {total_str:>20} {per_100_str:>15}")

    print("\n" + "=" * 60)
    print("\nNote: These are aggregate statistics for each income classification.")


def handle_filter_date(state):
    """Handle date range filter."""
    if state.current_data is None:
        print("\n✗ No data loaded. Please load data first (Option 1).")
        return

    from src.cli import parse_date_input
    from src.filters import filter_by_date_range

    print("\nEnter date range (YYYY-MM-DD format, leave blank to skip):")
    start = parse_date_input(get_user_input("Start date"))
    end = parse_date_input(get_user_input("End date"))

    if start is None and end is None:
        print("\n✗ No valid dates entered.")
        return

    filtered = filter_by_date_range(state.current_data, start, end)
    print(f"\n✓ Filtered to {len(filtered):,} records")

    if get_user_input("Use filtered data? (y/n)").lower() == "y":
        state.current_data = filtered
        print("✓ Now using filtered data.")


def handle_statistics(state):
    """Handle statistics view."""
    if state.current_data is None:
        print("\n✗ No data loaded. Please load data first (Option 1).")
        return

    numeric_cols = state.current_data.select_dtypes(include=["number"]).columns.tolist()
    column = display_column_menu(numeric_cols)

    if column not in state.current_data.columns:
        print(f"\n✗ Column '{column}' not found.")
        return

    stats = get_statistics(state, column)

    print("\n" + "=" * 55)
    print(f"Statistics for: {column}")
    if column in COLUMN_DESCRIPTIONS:
        print(f"  → {COLUMN_DESCRIPTIONS[column]}")
    print("=" * 55)

    unique_locations = state.current_data["location"].nunique()

    if unique_locations == 1:
        location = state.current_data["location"].iloc[0]
        print(f"\nLocation: {location}")
        print("\nTime Series Statistics:")
        print(f"   Records: {stats['count']:,}")
        print(f"   Mean:    {stats['mean']:,.2f}" if stats["mean"] else "   Mean: N/A")
        print(f"   Min:     {stats['min']:,.2f}" if stats["min"] else "   Min: N/A")
        print(f"   Max:     {stats['max']:,.2f}" if stats["max"] else "   Max: N/A")
    else:
        print(f"\nStatistics across {unique_locations} locations:")
        print(f"   Records: {stats['count']:,}")
        print(f"   Mean:    {stats['mean']:,.2f}" if stats["mean"] else "   Mean: N/A")
        print(f"   Min:     {stats['min']:,.2f}" if stats["min"] else "   Min: N/A")
        print(f"   Max:     {stats['max']:,.2f}" if stats["max"] else "   Max: N/A")

    print("=" * 55)


def handle_trends(state):
    """Handle trend analysis."""
    if state.current_data is None:
        print("\n✗ No data loaded. Please load data first (Option 1).")
        return

    country = display_country_menu()
    if not country:
        print("\n✗ No selection entered.")
        return

    trend = get_trend_analysis(state, country)

    if "error" in trend:
        print(f"\n✗ {trend['error']}")
        return

    print(f"\n{'=' * 50}")
    print(f"  {country} - Vaccination Trend Analysis")
    print(f"{'=' * 50}")

    print(
        f"\nDate Range: {trend['date_range']['start'].date()} to {trend['date_range']['end'].date()}"
    )
    print(f"Total Records: {trend['total_records']}")

    print("\nDaily Vaccinations Trend:")
    print(f"   Direction:      {trend['direction'].upper()}")
    print(f"   Start Value:    {trend['start_value']:,.0f}")
    print(f"   End Value:      {trend['end_value']:,.0f}")
    print(f"   Total Change:   {trend['total_change']:+,.0f}")
    print(f"   Percent Change: {trend['percent_change']:+.1f}%")

    print(f"{'=' * 50}")

    if get_user_input("Generate trend chart? (y/n)").lower() == "y":
        country_data = filter_data_by_country(state, [country]).sort_values("date")
        fig = create_line_chart(
            country_data,
            "date",
            "daily_vaccinations",
            f"{country} - Daily Vaccinations Trend",
        )
        os.makedirs("exports", exist_ok=True)
        filepath = f"exports/{country.replace(' ', '_')}_trend.png"
        save_chart(fig, filepath)
        print(f"\n✓ Chart saved to: {filepath}")
        plt.close(fig)


def handle_charts(state):
    """Handle chart generation."""
    if state.current_data is None:
        print("\n✗ No data loaded. Please load data first (Option 1).")
        return

    print("\nChart Types:")
    print("  1. Bar chart - Top Countries")
    print("  2. Line chart - Trend over time")

    choice = get_user_input("Select chart type (1-2)")

    os.makedirs("exports", exist_ok=True)

    if choice == "1":
        from src.visualizations import create_bar_chart
        from src.summaries import group_summary

        countries_only = get_countries_only(state.current_data)
        country_totals = group_summary(
            countries_only, "location", "total_vaccinations", "max"
        )
        top_10 = country_totals.nlargest(10).reset_index()
        top_10.columns = ["location", "total_vaccinations"]

        fig = create_bar_chart(
            top_10, "location", "total_vaccinations", "Top 10 Countries"
        )
        save_chart(fig, "exports/top_countries.png")
        print("\n✓ Chart saved to: exports/top_countries.png")
        plt.close(fig)
    elif choice == "2":
        handle_trends(state)


def handle_export(state):
    """Handle data export."""
    if state.current_data is None:
        print("\n✗ No data loaded. Please load data first (Option 1).")
        return

    os.makedirs("exports", exist_ok=True)
    filepath = "exports/filtered_data.csv"

    result = export_data(state, filepath)

    if result["success"]:
        print(f"\n✓ Exported {result['records']:,} records to: {result['filepath']}")
    else:
        print(f"\n✗ Error: {result['error']}")
