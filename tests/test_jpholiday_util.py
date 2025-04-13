from datetime import date

import polars as pl
from polars.testing import assert_series_equal


def test_is_holiday():
    """Test the ja.is_holidat expression."""
    data = [
        date(2023, 1, 1),
        date(2023, 1, 9),
        date(2023, 10, 10),
        date(2023, 11, 23),
        date(2024, 1, 2),
    ]
    series = pl.Series("test", data)
    expected_data = [True, True, False, True, False]
    expected = pl.Series("test", expected_data)

    # Apply the expression via the registered namespace
    df = series.to_frame()
    result_df = df.select(pl.col("test").ja.is_holiday())
    result = result_df.to_series()

    assert_series_equal(result, expected)


def test_is_business_day():
    """Test the ja.is_business_day expression."""
    data = [
        date(2023, 1, 1),
        date(2023, 1, 2),
        date(2023, 1, 3),
        date(2023, 1, 4),
        date(2023, 1, 9),
        date(2023, 10, 10),
        date(2023, 11, 23),
        date(2024, 1, 2),
    ]
    series = pl.Series("test", data)
    expected_data = [False, False, True, True, False, True, False, True]
    expected = pl.Series("test", expected_data)

    # Apply the expression via the registered namespace
    df = series.to_frame()
    result_df = df.select(pl.col("test").ja.is_business_day())
    result = result_df.to_series()

    assert_series_equal(result, expected)
