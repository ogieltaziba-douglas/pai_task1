"""
Tests for Constants Module

Tests to verify that all constants are correctly defined
and available for use across the application.
"""

import pytest


class TestAggregateKeywords:
    """Tests for AGGREGATE_KEYWORDS constant."""

    def test_aggregate_keywords_exists(self):
        """Test that AGGREGATE_KEYWORDS is defined."""
        from src.constants import AGGREGATE_KEYWORDS

        assert AGGREGATE_KEYWORDS is not None

    def test_aggregate_keywords_is_list(self):
        """Test that AGGREGATE_KEYWORDS is a list."""
        from src.constants import AGGREGATE_KEYWORDS

        assert isinstance(AGGREGATE_KEYWORDS, list)

    def test_aggregate_keywords_contains_world(self):
        """Test that World is in AGGREGATE_KEYWORDS."""
        from src.constants import AGGREGATE_KEYWORDS

        assert "World" in AGGREGATE_KEYWORDS

    def test_aggregate_keywords_contains_income(self):
        """Test that income identifier is in AGGREGATE_KEYWORDS."""
        from src.constants import AGGREGATE_KEYWORDS

        assert "income" in AGGREGATE_KEYWORDS


class TestContinents:
    """Tests for CONTINENTS constant."""

    def test_continents_exists(self):
        """Test that CONTINENTS is defined."""
        from src.constants import CONTINENTS

        assert CONTINENTS is not None

    def test_continents_is_list(self):
        """Test that CONTINENTS is a list."""
        from src.constants import CONTINENTS

        assert isinstance(CONTINENTS, list)

    def test_continents_has_six_items(self):
        """Test that there are 6 continents."""
        from src.constants import CONTINENTS

        assert len(CONTINENTS) == 6

    def test_continents_contains_europe(self):
        """Test that Europe is in CONTINENTS."""
        from src.constants import CONTINENTS

        assert "Europe" in CONTINENTS


class TestIncomeGroups:
    """Tests for INCOME_GROUPS constant."""

    def test_income_groups_exists(self):
        """Test that INCOME_GROUPS is defined."""
        from src.constants import INCOME_GROUPS

        assert INCOME_GROUPS is not None

    def test_income_groups_is_list(self):
        """Test that INCOME_GROUPS is a list."""
        from src.constants import INCOME_GROUPS

        assert isinstance(INCOME_GROUPS, list)

    def test_income_groups_has_four_items(self):
        """Test that there are 4 income groups."""
        from src.constants import INCOME_GROUPS

        assert len(INCOME_GROUPS) == 4

    def test_income_groups_contains_high_income(self):
        """Test that High income is in INCOME_GROUPS."""
        from src.constants import INCOME_GROUPS

        assert "High income" in INCOME_GROUPS


class TestKeyCountries:
    """Tests for KEY_COUNTRIES constant."""

    def test_key_countries_exists(self):
        """Test that KEY_COUNTRIES is defined."""
        from src.constants import KEY_COUNTRIES

        assert KEY_COUNTRIES is not None

    def test_key_countries_is_dict(self):
        """Test that KEY_COUNTRIES is a dictionary."""
        from src.constants import KEY_COUNTRIES

        assert isinstance(KEY_COUNTRIES, dict)

    def test_key_countries_has_six_continents(self):
        """Test that KEY_COUNTRIES has entries for 6 continents."""
        from src.constants import KEY_COUNTRIES

        assert len(KEY_COUNTRIES) == 6

    def test_key_countries_europe_has_countries(self):
        """Test that Europe has key countries."""
        from src.constants import KEY_COUNTRIES

        assert "Europe" in KEY_COUNTRIES
        assert len(KEY_COUNTRIES["Europe"]) >= 3

    def test_key_countries_contains_uk(self):
        """Test that UK is a key country in Europe."""
        from src.constants import KEY_COUNTRIES

        assert "United Kingdom" in KEY_COUNTRIES["Europe"]


class TestAllKeyCountries:
    """Tests for ALL_KEY_COUNTRIES constant."""

    def test_all_key_countries_exists(self):
        """Test that ALL_KEY_COUNTRIES is defined."""
        from src.constants import ALL_KEY_COUNTRIES

        assert ALL_KEY_COUNTRIES is not None

    def test_all_key_countries_is_list(self):
        """Test that ALL_KEY_COUNTRIES is a list."""
        from src.constants import ALL_KEY_COUNTRIES

        assert isinstance(ALL_KEY_COUNTRIES, list)

    def test_all_key_countries_has_correct_count(self):
        """Test that ALL_KEY_COUNTRIES has 24 countries."""
        from src.constants import ALL_KEY_COUNTRIES

        assert len(ALL_KEY_COUNTRIES) == 24

    def test_all_key_countries_contains_brazil(self):
        """Test that Brazil is in ALL_KEY_COUNTRIES."""
        from src.constants import ALL_KEY_COUNTRIES

        assert "Brazil" in ALL_KEY_COUNTRIES


class TestColumnDescriptions:
    """Tests for COLUMN_DESCRIPTIONS constant."""

    def test_column_descriptions_exists(self):
        """Test that COLUMN_DESCRIPTIONS is defined."""
        from src.constants import COLUMN_DESCRIPTIONS

        assert COLUMN_DESCRIPTIONS is not None

    def test_column_descriptions_is_dict(self):
        """Test that COLUMN_DESCRIPTIONS is a dictionary."""
        from src.constants import COLUMN_DESCRIPTIONS

        assert isinstance(COLUMN_DESCRIPTIONS, dict)

    def test_column_descriptions_has_total_vaccinations(self):
        """Test that total_vaccinations has a description."""
        from src.constants import COLUMN_DESCRIPTIONS

        assert "total_vaccinations" in COLUMN_DESCRIPTIONS
        assert len(COLUMN_DESCRIPTIONS["total_vaccinations"]) > 0

    def test_column_descriptions_has_daily_vaccinations(self):
        """Test that daily_vaccinations has a description."""
        from src.constants import COLUMN_DESCRIPTIONS

        assert "daily_vaccinations" in COLUMN_DESCRIPTIONS
