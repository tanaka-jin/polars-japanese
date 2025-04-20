import datetime as dt

import polars as pl
import pytest
from polars.testing import assert_series_equal

import polars_japanese  # noqa: F401


def test_expr_to_datetime_ignore_erros() -> None:
    """和暦を日付型に変換できることを確認(エラー無視)"""
    data = [
        "令和6年4月12日",
        "平成1年1月8日",
        "昭和64年1月7日",
        "昭和1年12月25日",
        "大正1年7月30日",
        "存在しない元号1年1月1日",
        None,
    ]
    series = pl.Series("date_str", data)
    df = series.to_frame()

    result_df = df.select(pl.col("date_str").ja.to_datetime(raise_error=False))
    result = result_df.to_series()

    expected_data = [
        dt.date(2024, 4, 12),
        dt.date(1989, 1, 8),
        dt.date(1989, 1, 7),
        dt.date(1926, 12, 25),
        dt.date(1912, 7, 30),
        None,
        None,
    ]
    expected = pl.Series("date_str", expected_data, dtype=pl.Date)

    assert_series_equal(result, expected)


def test_expr_to_datetime_raise_error() -> None:
    """和暦を日付型に変換できることを確認(エラー発生)"""
    data = [
        "令和6年4月12日",
        "平成1年1月8日",
        "昭和64年1月7日",
        "昭和1年12月25日",
        "大正1年7月30日",
        "存在しない元号1年1月1日",
        None,
    ]
    series = pl.Series("date_str", data)
    df = series.to_frame()

    with pytest.raises(Exception):
        df.select(pl.col("date_str").ja.to_datetime(raise_error=True))


def test_expr_to_datetime_with_format() -> None:
    """フォーマットを指定して和暦を日付型に変換できることを確認"""
    data = [
        "R6.04.12",
        "H1.01.08",
        "令和6年04月12日",
        "存在しない元号1年1月1日",
        None,
    ]
    series = pl.Series("date_str", data)
    df = series.to_frame()

    result_df = df.select(
        pl.col("date_str").ja.to_datetime(
            format="%-h%-y.%m.%d", raise_error=False
        )
    )
    result = result_df.to_series()

    expected_data = [
        dt.date(2024, 4, 12),
        dt.date(1989, 1, 8),
        None,
        None,
        None,
    ]
    expected = pl.Series("date_str", expected_data, dtype=pl.Date)

    assert_series_equal(result, expected)


def test_expr_to_wareki() -> None:
    """日付型を和暦に変換できることを確認"""
    data = [
        dt.date(2024, 4, 12),
        dt.date(1989, 1, 8),
        dt.date(1989, 1, 7),
        dt.date(1926, 12, 25),
        dt.date(1912, 7, 30),
        None,
    ]
    series = pl.Series("date", data, dtype=pl.Date)
    df = series.to_frame()

    result_df = df.select(pl.col("date").ja.to_wareki())
    result = result_df.to_series()

    expected_data = [
        "令和6年04月12日",
        "平成1年01月08日",
        "昭和64年01月07日",
        "昭和1年12月25日",
        "大正1年07月30日",
        None,
    ]
    expected = pl.Series("date", expected_data, dtype=pl.Utf8)

    assert_series_equal(result, expected)


def test_expr_to_wareki_with_format() -> None:
    """フォーマットを指定して日付型を和暦に変換できることを確認"""
    data = [
        dt.date(2024, 4, 12),
        dt.date(1989, 1, 8),
        dt.date(1989, 1, 7),
        None,
    ]
    series = pl.Series("date", data, dtype=pl.Date)
    df = series.to_frame()

    result_df = df.select(pl.col("date").ja.to_wareki(format="%-h%-Y.%m.%d"))
    result = result_df.to_series()

    expected_data = [
        "R6.04.12",
        "H1.01.08",
        "S64.01.07",
        None,
    ]
    expected = pl.Series("date", expected_data, dtype=pl.Utf8)

    assert_series_equal(result, expected)
