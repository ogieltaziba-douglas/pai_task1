"""
Constants Module

This module contains all configuration constants used across
the Public Health Data Insights Dashboard application.

Constants:
    AGGREGATE_KEYWORDS: Keywords to identify aggregate/regional data
    CONTINENTS: List of continent names
    INCOME_GROUPS: List of income group classifications
    KEY_COUNTRIES: Dictionary of key countries per continent
    ALL_KEY_COUNTRIES: Flat list of all key countries
    COLUMN_DESCRIPTIONS: Descriptions for each data column
"""

# Keywords to identify aggregate entries (not actual countries)
AGGREGATE_KEYWORDS = [
    "income",
    "World",
    "Europe",
    "Asia",
    "Africa",
    "America",
    "Oceania",
    "European Union",
    "North America",
    "South America",
]

# List of continents
CONTINENTS = [
    "Europe",
    "Asia",
    "Africa",
    "North America",
    "South America",
    "Oceania",
]

# Income group classifications
INCOME_GROUPS = [
    "High income",
    "Upper middle income",
    "Lower middle income",
    "Low income",
]

# Key countries per continent (major/representative countries)
KEY_COUNTRIES = {
    "Europe": ["United Kingdom", "Germany", "France", "Italy", "Spain"],
    "Asia": ["China", "India", "Japan", "Indonesia", "South Korea"],
    "Africa": ["South Africa", "Nigeria", "Egypt", "Kenya", "Morocco"],
    "North America": ["United States", "Canada", "Mexico"],
    "South America": ["Brazil", "Argentina", "Colombia", "Chile"],
    "Oceania": ["Australia", "New Zealand"],
}

# Flat list of all key countries
ALL_KEY_COUNTRIES = [
    country for countries in KEY_COUNTRIES.values() for country in countries
]

# Descriptions for each column to help users understand the data
COLUMN_DESCRIPTIONS = {
    "total_vaccinations": "Total number of vaccine doses administered (cumulative)",
    "people_vaccinated": "Total number of people who received at least one dose",
    "people_fully_vaccinated": "Total number of people who completed their primary vaccination",
    "total_boosters": "Total number of booster doses administered",
    "daily_vaccinations_raw": "Daily doses administered (raw, unsmoothed)",
    "daily_vaccinations": "Daily doses administered (7-day rolling average)",
    "total_vaccinations_per_hundred": "Total doses per 100 people in the population",
    "people_vaccinated_per_hundred": "People with at least one dose per 100 people",
    "people_fully_vaccinated_per_hundred": "Fully vaccinated people per 100 people",
    "total_boosters_per_hundred": "Booster doses per 100 people",
    "daily_vaccinations_per_million": "Daily doses per million people (7-day average)",
    "daily_people_vaccinated": "Daily new people receiving first dose (7-day average)",
    "daily_people_vaccinated_per_hundred": "Daily new vaccinees per 100 people",
}
