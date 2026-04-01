import pytest

from pse_sdk._dates import normalize_date, normalize_date_range, split_date_range


class TestNormalizeDate:
    def test_yyyy_mm_dd(self):
        assert normalize_date("2024-01-15", "d") == "2024-01-15"

    def test_yyyy_slash(self):
        assert normalize_date("2024/01/15", "d") == "2024-01-15"

    def test_yyyymmdd(self):
        assert normalize_date("20240115", "d") == "2024-01-15"

    def test_whitespace_stripped(self):
        assert normalize_date("  2024-01-15  ", "d") == "2024-01-15"

    def test_invalid_string(self):
        with pytest.raises(ValueError, match="start"):
            normalize_date("not-a-date", "start")

    def test_wrong_type(self):
        with pytest.raises(TypeError, match="end"):
            normalize_date(12345, "end")

    def test_impossible_date(self):
        with pytest.raises(ValueError):
            normalize_date("2024-02-30", "d")


class TestNormalizeDateRange:
    def test_equal_dates_pass(self):
        assert normalize_date_range("2024-01-01", "2024-01-01") == ("2024-01-01", "2024-01-01")

    def test_start_before_end_pass(self):
        assert normalize_date_range("2024-01-01", "2024-01-31") == ("2024-01-01", "2024-01-31")

    def test_start_after_end_raises(self):
        with pytest.raises(ValueError, match="must not be after"):
            normalize_date_range("2024-02-01", "2024-01-01")


class TestSplitDateRange:
    def test_single_chunk_within_max_days(self):
        assert split_date_range("2024-01-01", "2024-01-20") == [
            ("2024-01-01", "2024-01-20")
        ]

    def test_exact_max_days(self):
        assert split_date_range("2024-01-01", "2024-01-30", max_days=30) == [
            ("2024-01-01", "2024-01-30")
        ]

    def test_two_chunks(self):
        assert split_date_range("2024-01-01", "2024-02-29") == [
            ("2024-01-01", "2024-01-30"),
            ("2024-01-31", "2024-02-29"),
        ]

    def test_same_day(self):
        assert split_date_range("2024-01-01", "2024-01-01") == [
            ("2024-01-01", "2024-01-01")
        ]

    def test_last_chunk_shorter(self):
        result = split_date_range("2024-01-01", "2024-02-14")
        assert result == [
            ("2024-01-01", "2024-01-30"),
            ("2024-01-31", "2024-02-14"),
        ]

    def test_custom_max_days(self):
        assert split_date_range("2024-01-01", "2024-01-14", max_days=7) == [
            ("2024-01-01", "2024-01-07"),
            ("2024-01-08", "2024-01-14"),
        ]
