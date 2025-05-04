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
    """ja.normalize をテストします。NFKC + 日本語特有ルール"""
    data = [
        "ﾃｽﾄ",  # 半角カナ -> 全角カナ
        "ＡＢＣ",  # 全角英数 -> 半角英数
        "１２３",  # 全角数字 -> 半角数字
        "ﾊﾝｶｸ　スペース",  # 半角カナ + 全角スペース
        "スーパー‐ハイフン-マイナス",  # 様々なハイフン -> 半角ハイフン
        "チルダ~と全角チルダ～",  # チルダ -> 全角チルダ
        "感嘆符！ビックリマーク!",  # 感嘆符 -> 半角
        "疑問符？クエスチョン？",  # 疑問符 -> 半角
        "スペース　　連続　",  # 全角・連続スペース -> 半角スペース
        "　　スペース外側　",  # トリム
        "㈱",  # 特殊文字 (NFKCで変換)
        None,
    ]
    series = pl.Series("test", data)
    expected_data = [
        "テスト",
        "ABC",
        "123",
        "ハンカク スペース",
        "スーパー-ハイフン-マイナス",
        "チルダ~と全角チルダ~",
        "感嘆符!ビックリマーク!",
        "疑問符?クエスチョン?",
        "スペース 連続",
        "スペース外側",
        "(株)",
        None,
    ]
    expected = pl.Series("test", expected_data)

    df = series.to_frame()
    result_df = df.select(pl.col("test").ja.normalize())
    result = result_df.to_series()
    assert_series_equal(result, expected)
