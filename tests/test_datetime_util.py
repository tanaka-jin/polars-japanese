from datetime import date, datetime

import polars as pl
import polars_japanese  # noqa: F401
import pytest
from polars.testing import assert_frame_equal


def test_to_japanese_weekday_date_default_format():
    df = pl.DataFrame(
        {
            "dates": [
                date(2024, 5, 10),  # 金曜日
                date(2024, 5, 13),  # 月曜日
                None,
            ]
        }
    )
    expected = pl.DataFrame(
        {
            "dates": [
                date(2024, 5, 10),
                date(2024, 5, 13),
                None,
            ],
            "weekday_ja": ["金曜日", "月曜日", None],
        }
    ).with_columns(pl.col("weekday_ja").cast(pl.String))
    result = df.with_columns(weekday_ja=pl.col("dates").ja.to_weekday_name())
    assert_frame_equal(result, expected, check_dtypes=True)


def test_to_japanese_weekday_date_format_A():
    df = pl.DataFrame({"dates": [date(2024, 5, 10)]})  # 金曜日
    expected = pl.DataFrame({"dates": [date(2024, 5, 10)], "weekday_ja": ["金曜日"]})
    result = df.with_columns(weekday_ja=pl.col("dates").ja.to_weekday_name(format="%A"))
    assert_frame_equal(result, expected, check_dtypes=True)


def test_to_japanese_weekday_date_format_a():
    df = pl.DataFrame({"dates": [date(2024, 5, 10)]})  # 金
    expected = pl.DataFrame({"dates": [date(2024, 5, 10)], "weekday_ja": ["金"]})
    result = df.with_columns(weekday_ja=pl.col("dates").ja.to_weekday_name(format="%a"))
    assert_frame_equal(result, expected, check_dtypes=True)


def test_to_japanese_weekday_datetime_default_format():
    df = pl.DataFrame(
        {
            "datetimes": [
                datetime(2024, 5, 12, 10, 30, 0),  # 日曜日
                None,
            ]
        }
    )
    expected = pl.DataFrame(
        {
            "datetimes": [
                datetime(2024, 5, 12, 10, 30, 0),
                None,
            ],
            "weekday_ja": ["日曜日", None],
        }
    ).with_columns(pl.col("weekday_ja").cast(pl.String))
    result = df.with_columns(weekday_ja=pl.col("datetimes").ja.to_weekday_name())
    assert_frame_equal(result, expected, check_dtypes=True)


def test_to_japanese_weekday_datetime_format_A():
    df = pl.DataFrame({"datetimes": [datetime(2024, 5, 12, 10, 30, 0)]})  # 日曜日
    expected = pl.DataFrame(
        {"datetimes": [datetime(2024, 5, 12, 10, 30, 0)], "weekday_ja": ["日曜日"]}
    )
    result = df.with_columns(
        weekday_ja=pl.col("datetimes").ja.to_weekday_name(format="%A")
    )
    assert_frame_equal(result, expected, check_dtypes=True)


def test_to_japanese_weekday_datetime_format_a():
    df = pl.DataFrame({"datetimes": [datetime(2024, 5, 12, 10, 30, 0)]})  # 日
    expected = pl.DataFrame(
        {"datetimes": [datetime(2024, 5, 12, 10, 30, 0)], "weekday_ja": ["日"]}
    )
    result = df.with_columns(
        weekday_ja=pl.col("datetimes").ja.to_weekday_name(format="%a")
    )
    assert_frame_equal(result, expected, check_dtypes=True)


def test_to_japanese_weekday_empty():
    df = pl.DataFrame({"dates": pl.Series([], dtype=pl.Date)})
    expected = pl.DataFrame(
        {
            "dates": pl.Series([], dtype=pl.Date),
            "weekday_ja": pl.Series([], dtype=pl.String),
        }
    )
    result = df.with_columns(weekday_ja=pl.col("dates").ja.to_weekday_name())
    assert_frame_equal(result, expected, check_dtypes=True)


def test_to_japanese_weekday_all_null():
    df = pl.DataFrame({"dates": pl.Series([None, None], dtype=pl.Date)})
    expected = pl.DataFrame(
        {
            "dates": pl.Series([None, None], dtype=pl.Date),
            "weekday_ja": pl.Series([None, None], dtype=pl.String),
        }
    )
    result = df.with_columns(weekday_ja=pl.col("dates").ja.to_weekday_name())
    assert_frame_equal(result, expected, check_dtypes=True)


def test_to_japanese_weekday_invalid_format():
    df = pl.DataFrame({"dates": [date(2024, 5, 10)]})
    with pytest.raises(
        ValueError,
        match="Unsupported format string: %X. Supported formats: '%A', '%a'.",
    ):
        df.with_columns(weekday_ja=pl.col("dates").ja.to_weekday_name(format="%X"))


def test_weekday_values():
    # Polars weekday(): 1 (Mon) to 7 (Sun)
    dates = [date(2024, 5, 13 + i) for i in range(7)]  # Mon to Sun
    df = pl.DataFrame({"dates": dates})
    expected_full = pl.Series(
        "weekday_full",
        ["月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日", "日曜日"],
    )
    expected_short = pl.Series(
        "weekday_short", ["月", "火", "水", "木", "金", "土", "日"]
    )

    result_full = df.select(
        pl.col("dates").ja.to_weekday_name(format="%A").alias("weekday_full")
    )
    result_short = df.select(
        pl.col("dates").ja.to_weekday_name(format="%a").alias("weekday_short")
    )

    assert_frame_equal(result_full, expected_full.to_frame(), check_dtypes=True)
    assert_frame_equal(result_short, expected_short.to_frame(), check_dtypes=True)
