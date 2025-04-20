import polars as pl
from polars.testing import assert_series_equal

import polars_japanese  # noqa: F401


def test_to_half_width():
    """ja.to_half_width 式をテストします。"""
    data = [
        "アイウエオ",
        "ｶﾞｷﾞｸﾞｹﾞｺﾞ",
        "１２３４５",
        "ＡＢＣＤＥ",
        "　",
        "ひらがな",
        "漢字",
        "記号！＠＃",
        None,
    ]
    series = pl.Series("test", data)
    expected_data = [
        "ｱｲｳｴｵ",
        "ｶﾞｷﾞｸﾞｹﾞｺﾞ",
        "12345",
        "ABCDE",
        " ",
        "ひらがな",
        "漢字",
        "記号!@#",
        None,
    ]
    expected = pl.Series("test", expected_data)

    # Apply the expression via the registered namespace
    df = series.to_frame()
    result_df = df.select(pl.col("test").ja.to_half_width())
    result = result_df.to_series()

    assert_series_equal(result, expected)


def test_to_full_width():
    """ja.to_full_width 式をテストします。"""
    data = [
        "ｱｲｳｴｵ",
        "ｶﾞｷﾞｸﾞｹﾞｺﾞ",
        "12345",
        "ABCDE",
        " ",
        "ひらがな",
        "漢字",
        "記号！＠＃",
        None,
    ]
    series = pl.Series("test", data)
    expected_data = [
        "アイウエオ",
        "ガギグゲゴ",
        "１２３４５",
        "ＡＢＣＤＥ",
        "　",
        "ひらがな",
        "漢字",
        "記号！＠＃",
        None,
    ]
    expected = pl.Series("test", expected_data)

    # Apply the expression via the registered namespace
    df = series.to_frame()
    result_df = df.select(pl.col("test").ja.to_full_width())
    result = result_df.to_series()

    assert_series_equal(result, expected)


def test_to_half_width_mixed():
    """ja.to_half_width を混合文字でテストします。"""
    data = [
        "全角スペース　と半角スペース ",
        "数字１２３と数字123",
        "カタカナアイウとｶﾀｶﾅｱｲｳ",
    ]
    series = pl.Series("test", data)
    expected_data = [
        "全角ｽﾍﾟｰｽ と半角ｽﾍﾟｰｽ ",
        "数字123と数字123",
        "ｶﾀｶﾅｱｲｳとｶﾀｶﾅｱｲｳ",
    ]
    expected = pl.Series("test", expected_data)

    df = series.to_frame()
    result_df = df.select(pl.col("test").ja.to_half_width())
    result = result_df.to_series()
    assert_series_equal(result, expected)


def test_to_full_width_mixed():
    """ja.to_full_width を混合文字でテストします。"""
    data = [
        "全角スペース　と半角スペース ",
        "数字１２３と数字123",
        "カタカナアイウとｶﾀｶﾅｱｲｳ",
    ]
    series = pl.Series("test", data)
    expected_data = [
        "全角スペース　と半角スペース　",
        "数字１２３と数字１２３",
        "カタカナアイウとカタカナアイウ",
    ]
    expected = pl.Series("test", expected_data)

    df = series.to_frame()
    result_df = df.select(pl.col("test").ja.to_full_width())
    result = result_df.to_series()
    assert_series_equal(result, expected)


def test_normalize():
    """ja.normalize をテストします。"""
    data = ["ﾃｽﾄ", "ＡＢＣ", "123"]
    series = pl.Series("test", data)
    expected_data = ["テスト", "ABC", "123"]
    expected = pl.Series("test", expected_data)

    df = series.to_frame()
    result_df = df.select(pl.col("test").ja.normalize())
    result = result_df.to_series()
    assert_series_equal(result, expected)
