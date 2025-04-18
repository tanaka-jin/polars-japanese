import polars as pl
from polars.testing import assert_series_equal

import polars_japanese.common  # noqa: F401


def test_to_kanji():
    """Test the ja.to_kanji expression."""
    data = [123, None]
    series = pl.Series("test", data)
    expected_data = ["百二十三", None]
    expected = pl.Series("test", expected_data)

    # Apply the expression via the registered namespace
    df = series.to_frame()
    result_df = df.select(pl.col("test").ja.to_kanji())
    result = result_df.to_series()

    assert_series_equal(result, expected)


def test_to_number():
    """Test the ja.to_number expression."""
    data = ["百二十三", None]
    series = pl.Series("test", data)
    expected_data = [123, None]
    expected = pl.Series("test", expected_data, dtype=pl.Int64)

    # Apply the expression via the registered namespace
    df = series.to_frame()
    result_df = df.select(pl.col("test").ja.to_number())
    result = result_df.to_series()

    assert_series_equal(result, expected)
