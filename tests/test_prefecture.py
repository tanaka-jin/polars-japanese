import polars as pl
import polars_japanese  # noqa: F401
import pytest
from polars.testing import assert_frame_equal


def test_to_code():
    # 都道府県名からコードへの変換テスト
    data_names = {
        "pref_name": [
            "北海道",
            "青森",
            "iwate",
            "MIYAGI",
            "秋田県",
            "やまがたけん",
            "フクシマ",
            "IBARAKI",
            "とちぎ",
            "グンマケン",
            "Saitama",
            "ちばけん",
            "東京",
            "kanagawa",
            "富山県",
            "石川",
            "Fukui",
            "やまなし",
            "ナガノケン",
            "Gifu",
            "しずおか",
            "アイチ",
            "Mie",
            "滋賀県",
            "きょうとふ",
            "オオサカフ",
            "Hyogo",
            "ならけん",
            "ワカヤマ",
            "Tottori",
            "しまね",
            "オカヤマケン",
            "Hiroshima",
            "やまぐちけん",
            "トクシマ",
            "Kagawa",
            "えひめ",
            "コウチケン",
            "Fukuoka",
            "さがけん",
            "ﾅｶﾞｻｷ",
            "Kumamoto",
            "おおいた",
            "ミヤザキケン",
            "Kagoshima",
            "おきなわ",
            "存在しない県",
            None,
        ],
    }
    df_names = pl.DataFrame(data_names)
    expected_codes = [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        16,
        17,
        18,
        19,
        20,
        21,
        22,
        23,
        24,
        25,
        26,
        27,
        28,
        29,
        30,
        31,
        32,
        33,
        34,
        35,
        36,
        37,
        38,
        39,
        40,
        41,
        42,
        43,
        44,
        45,
        46,
        47,
        None,
        None,
    ]
    expected_df_names = pl.DataFrame(
        {"pref_name": expected_codes}, schema={"pref_name": pl.Int64}
    )
    result_df_names = df_names.with_columns(
        pl.col("pref_name").ja_pref.to_code()
    )
    assert_frame_equal(result_df_names, expected_df_names, check_dtypes=True)

    # 都道府県コード(文字列)からコードへの変換テスト
    data_codes_str = {
        "pref_name": ["1", "15", "47", "99", None],
    }
    df_codes_str = pl.DataFrame(data_codes_str)
    expected_codes_from_str = [1, 15, 47, None, None]
    expected_df_codes_str = pl.DataFrame(
        {"pref_name": expected_codes_from_str}, schema={"pref_name": pl.Int64}
    )
    result_df_codes_str = df_codes_str.with_columns(
        pl.col("pref_name").ja_pref.to_code()
    )
    assert_frame_equal(
        result_df_codes_str, expected_df_codes_str, check_dtypes=True
    )


def test_to_kanji_from_code():
    # コード(文字列)から漢字への変換テスト
    data = {"pref_code": ["1", "13", "47", "99", None]}
    df = pl.DataFrame(data)
    expected = pl.DataFrame(
        {"pref_code": ["北海道", "東京都", "沖縄県", None, None]}
    )
    result_df = df.with_columns(pl.col("pref_code").ja_pref.to_kanji())
    assert_frame_equal(result_df, expected)


def test_to_kanji_from_name():
    # 他の表記の都道府県名から漢字への変換テスト
    data = {
        "pref_code": [
            "ほっかいどう",
            "TOKYO",
            "おおさかふ",
            "存在しない県",
            None,
        ]
    }
    df = pl.DataFrame(data)
    expected = pl.DataFrame(
        {"pref_code": ["北海道", "東京都", "大阪府", None, None]}
    )
    result_df = df.with_columns(pl.col("pref_code").ja_pref.to_kanji())
    assert_frame_equal(result_df, expected)


def test_to_hiragana_from_code():
    # コード(文字列)からひらがなへの変換テスト
    data = {"pref_code": ["1", "13", "27", "99", None]}
    df = pl.DataFrame(data)
    expected = pl.DataFrame(
        {
            "pref_code": [
                "ほっかいどう",
                "とうきょうと",
                "おおさかふ",
                None,
                None,
            ]
        }
    )
    result_df = df.with_columns(pl.col("pref_code").ja_pref.to_hiragana())
    assert_frame_equal(result_df, expected)


def test_to_hiragana_from_name():
    # 他の表記の都道府県名からひらがなへの変換テスト
    data = {
        "pref_code": ["北海道", "TOKYO", "オオサカフ", "存在しない県", None]
    }
    df = pl.DataFrame(data)
    expected = pl.DataFrame(
        {
            "pref_code": [
                "ほっかいどう",
                "とうきょうと",
                "おおさかふ",
                None,
                None,
            ]
        }
    )
    result_df = df.with_columns(pl.col("pref_code").ja_pref.to_hiragana())
    assert_frame_equal(result_df, expected)


def test_to_katakana_from_code():
    # コード(文字列)からカタカナへの変換テスト
    data = {"pref_code": ["1", "13", "27", "99", None]}
    df = pl.DataFrame(data)
    expected = pl.DataFrame(
        {
            "pref_code": [
                "ホッカイドウ",
                "トウキョウト",
                "オオサカフ",
                None,
                None,
            ]
        }
    )
    result_df = df.with_columns(pl.col("pref_code").ja_pref.to_katakana())
    assert_frame_equal(result_df, expected)


def test_to_katakana_from_name():
    # 他の表記の都道府県名からカタカナへの変換テスト
    data = {
        "pref_code": ["北海道", "tokyo", "おおさかふ", "存在しない県", None]
    }
    df = pl.DataFrame(data)
    expected = pl.DataFrame(
        {
            "pref_code": [
                "ホッカイドウ",
                "トウキョウト",
                "オオサカフ",
                None,
                None,
            ]
        }
    )
    result_df = df.with_columns(pl.col("pref_code").ja_pref.to_katakana())
    assert_frame_equal(result_df, expected)


def test_to_romaji_from_code():
    # コード(文字列)からローマ字への変換テスト
    data = {"pref_code": ["1", "13", "27", "99", None]}
    df = pl.DataFrame(data)
    expected = pl.DataFrame(
        {"pref_code": ["HOKKAIDO", "TOKYO", "OSAKA", None, None]}
    )
    result_df = df.with_columns(pl.col("pref_code").ja_pref.to_romaji())
    assert_frame_equal(result_df, expected)


def test_to_romaji_from_name():
    # 他の表記の都道府県名からローマ字への変換テスト
    data = {
        "pref_code": [
            "北海道",
            "とうきょうと",
            "オオサカフ",
            "存在しない県",
            None,
        ]
    }
    df = pl.DataFrame(data)
    expected = pl.DataFrame(
        {"pref_code": ["HOKKAIDO", "TOKYO", "OSAKA", None, None]}
    )
    result_df = df.with_columns(pl.col("pref_code").ja_pref.to_romaji())
    assert_frame_equal(result_df, expected)


def test_to_region_from_code():
    # コード(文字列)から地方への変換テスト
    data = {"pref_code": ["1", "13", "27", "40", "99", None]}
    df = pl.DataFrame(data)
    expected = pl.DataFrame(
        {"pref_code": ["北海道", "関東", "近畿", "九州・沖縄", None, None]}
    )
    result_df = df.with_columns(pl.col("pref_code").ja_pref.to_region())
    assert_frame_equal(result_df, expected)


def test_to_region_from_name():
    # 他の表記の都道府県名から地方への変換テスト
    data = {
        "pref_code": [
            "北海道",
            "tokyo",
            "大阪府",
            "FUKUOKA",
            "存在しない県",
            None,
        ]
    }
    df = pl.DataFrame(data)
    expected = pl.DataFrame(
        {"pref_code": ["北海道", "関東", "近畿", "九州・沖縄", None, None]}
    )
    result_df = df.with_columns(pl.col("pref_code").ja_pref.to_region())
    assert_frame_equal(result_df, expected)


@pytest.mark.parametrize(
    "input_val, method_name, expected_val",
    [
        # to_code
        ("北海道", "to_code", 1),
        ("HOKKAIDO", "to_code", 1),
        ("ほっかいどう", "to_code", 1),
        ("ホッカイドウ", "to_code", 1),
        ("青森", "to_code", 2),
        ("青森県", "to_code", 2),
        ("AOMORI", "to_code", 2),
        ("aomori", "to_code", 2),
        ("あおもり", "to_code", 2),
        ("アオモリ", "to_code", 2),
        ("13", "to_code", 13),  # 数値での入力(文字列)
        ("東京", "to_code", 13),
        ("東京都", "to_code", 13),
        ("TOKYO", "to_code", 13),
        ("tokyo", "to_code", 13),
        ("とうきょう", "to_code", 13),
        ("トウキョウ", "to_code", 13),
        ("存在しない", "to_code", None),
        ("99", "to_code", None),  # 存在しないコード (文字列)
        # to_kanji
        ("1", "to_kanji", "北海道"),
        ("HOKKAIDO", "to_kanji", "北海道"),
        ("青森", "to_kanji", "青森県"),
        ("13", "to_kanji", "東京都"),
        ("tokyo", "to_kanji", "東京都"),
        ("存在しない", "to_kanji", None),
        # to_hiragana
        ("1", "to_hiragana", "ほっかいどう"),
        ("HOKKAIDO", "to_hiragana", "ほっかいどう"),
        ("青森", "to_hiragana", "あおもりけん"),
        ("13", "to_hiragana", "とうきょうと"),
        ("tokyo", "to_hiragana", "とうきょうと"),
        # to_katakana
        ("1", "to_katakana", "ホッカイドウ"),
        ("HOKKAIDO", "to_katakana", "ホッカイドウ"),
        ("青森", "to_katakana", "アオモリケン"),
        ("13", "to_katakana", "トウキョウト"),
        ("tokyo", "to_katakana", "トウキョウト"),
        # to_romaji
        ("1", "to_romaji", "HOKKAIDO"),
        ("北海道", "to_romaji", "HOKKAIDO"),
        ("あおもりけん", "to_romaji", "AOMORI"),
        ("13", "to_romaji", "TOKYO"),
        ("トウキョウト", "to_romaji", "TOKYO"),
        # to_region
        ("1", "to_region", "北海道"),
        ("HOKKAIDO", "to_region", "北海道"),
        ("2", "to_region", "東北"),
        ("青森", "to_region", "東北"),
        ("13", "to_region", "関東"),
        ("tokyo", "to_region", "関東"),
        ("27", "to_region", "近畿"),
        ("OSAKA", "to_region", "近畿"),
        ("40", "to_region", "九州・沖縄"),
        ("Fukuoka", "to_region", "九州・沖縄"),
    ],
)
def test_expr_methods_scalar(input_val, method_name, expected_val):
    df = pl.DataFrame(
        {"a": [str(input_val) if isinstance(input_val, int) else input_val]}
    )  # 入力値を文字列に統一
    expr = getattr(pl.col("a").ja_pref, method_name)()
    result_series = df.select(expr).to_series()

    result = result_series[0]
    # to_code の結果は数値なので、期待値も数値で比較
    if method_name == "to_code" and expected_val is not None:
        assert result == expected_val
    # それ以外は文字列なので、そのまま比較
    elif method_name == "to_code" and expected_val is None:
        assert result is None
    else:
        assert result == expected_val
