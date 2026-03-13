import sys

import pandas as pd
import pytest

from pse_sdk._format import convert, to_dataframe, validate_format


class TestValidateFormat:
    def test_dict_accepted(self):
        validate_format("dict")

    def test_dataframe_accepted(self):
        validate_format("dataframe")

    def test_invalid_raises(self):
        with pytest.raises(ValueError, match="format must be"):
            validate_format("csv")


class TestToDataframe:
    def test_non_empty_records(self):
        records = [{"a": 1, "b": 2}, {"a": 3, "b": 4}]
        df = to_dataframe(records)
        assert df.shape == (2, 2)

    def test_empty_list(self):
        df = to_dataframe([])
        assert len(df) == 0

    def test_return_type(self):
        result = to_dataframe([{"x": 1}])
        assert isinstance(result, pd.DataFrame)

    def test_import_error_when_pandas_missing(self, monkeypatch):
        monkeypatch.setitem(sys.modules, "pandas", None)
        with pytest.raises(ImportError, match="pandas is required"):
            to_dataframe([{"x": 1}])


class TestConvert:
    def test_dict_returns_list_as_is(self):
        data = [{"a": 1}]
        assert convert(data, "dict") is data

    def test_dataframe_returns_df(self):
        result = convert([{"a": 1}], "dataframe")
        assert isinstance(result, pd.DataFrame)

    def test_invalid_format_raises(self):
        with pytest.raises(ValueError):
            convert([], "xml")
