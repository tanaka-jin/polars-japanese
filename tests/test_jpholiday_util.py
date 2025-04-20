from datetime import date

import polars as pl
from polars.testing import assert_series_equal

import polars_japanese  # noqa: F401


def test_is_holiday():
    """祝日判定ができることを確認"""
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
    """営業日判定ができることを確認"""
    data = [
        date(2023, 1, 1),  # 祝日
        date(2023, 1, 2),  # 振替休日
        date(2023, 1, 3),  # 火曜日
        date(2023, 1, 4),  # 水曜日
        date(2023, 1, 7),  # 土曜日
        date(2023, 1, 8),  # 日曜日
        date(2023, 1, 9),  # 祝日
        date(2023, 10, 10),  # 火曜日
        date(2023, 11, 23),  # 祝日
        date(2024, 1, 2),  # 火曜日
    ]
    series = pl.Series("test", data)
    expected_data = [
        False,  # 祝日
        False,  # 月曜日
        True,  # 火曜日
        True,  # 水曜日
        False,  # 土曜日
        False,  # 日曜日
        False,  # 祝日
        True,  # 火曜日
        False,  # 祝日
        True,  # 火曜日
    ]
    expected = pl.Series("test", expected_data)

    # Apply the expression via the registered namespace
    df = series.to_frame()
    result_df = df.select(pl.col("test").ja.is_business_day())
    result = result_df.to_series()

    assert_series_equal(result, expected)
