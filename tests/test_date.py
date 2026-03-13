import datetime

import pytest

from pse_sdk._dates import normalize_date, normalize_date_range


class TestNormalizeDate:
    def test_yyyy_mm_dd(self):
        assert normalize_date("2024-01-15", "d") == "2024-01-15"

    def test_yyyy_slash(self):
        assert normalize_date("2024/01/15", "d") == "2024-01-15"

    def test_yyyymmdd(self):
        assert normalize_date("20240115", "d") == "2024-01-15"

    def test_whitespace_stripped(self):
        assert normalize_date("  2024-01-15  ", "d") == "2024-01-15"

    def test_date_object(self):
        assert normalize_date(datetime.date(2024, 1, 15), "d") == "2024-01-15"

    def test_datetime_object(self):
        dt = datetime.datetime(2024, 1, 15, 13, 45, 0)
        assert normalize_date(dt, "d") == "2024-01-15"

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

    def test_mixed_types(self):
        import datetime
        result = normalize_date_range(datetime.date(2024, 1, 1), "20240131")
        assert result == ("2024-01-01", "2024-01-31")
