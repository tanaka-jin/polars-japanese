from typing import Union

import polars as pl
from polars.api import register_expr_namespace

# --- データ定義 ---
# 都道府県コードから各種表記へのマッピング
# fmt: off
_PREFECTURE_DATA: dict[int, dict[str, Union[str, int]]] = {
    1: {"code": 1, "kanji": "北海道", "hira": "ほっかいどう", "kana": "ホッカイドウ", "roman": "HOKKAIDO", "region": "北海道"},  # noqa: E501
    2: {"code": 2, "kanji": "青森県", "hira": "あおもりけん", "kana": "アオモリケン", "roman": "AOMORI", "region": "東北"},  # noqa: E501
    3: {"code": 3, "kanji": "岩手県", "hira": "いわてけん", "kana": "イワテケン", "roman": "IWATE", "region": "東北"},  # noqa: E501
    4: {"code": 4, "kanji": "宮城県", "hira": "みやぎけん", "kana": "ミヤギケン", "roman": "MIYAGI", "region": "東北"},  # noqa: E501
    5: {"code": 5, "kanji": "秋田県", "hira": "あきたけん", "kana": "アキタケン", "roman": "AKITA", "region": "東北"},  # noqa: E501
    6: {"code": 6, "kanji": "山形県", "hira": "やまがたけん", "kana": "ヤマガタケン", "roman": "YAMAGATA", "region": "東北"},  # noqa: E501
    7: {"code": 7, "kanji": "福島県", "hira": "ふくしまけん", "kana": "フクシマケン", "roman": "FUKUSHIMA", "region": "東北"},  # noqa: E501
    8: {"code": 8, "kanji": "茨城県", "hira": "いばらきけん", "kana": "イバラキケン", "roman": "IBARAKI", "region": "関東"},  # noqa: E501
    9: {"code": 9, "kanji": "栃木県", "hira": "とちぎけん", "kana": "トチギケン", "roman": "TOCHIGI", "region": "関東"},  # noqa: E501
    10: {"code": 10, "kanji": "群馬県", "hira": "ぐんまけん", "kana": "グンマケン", "roman": "GUNMA", "region": "関東"},  # noqa: E501
    11: {"code": 11, "kanji": "埼玉県", "hira": "さいたまけん", "kana": "サイタマケン", "roman": "SAITAMA", "region": "関東"},  # noqa: E501
    12: {"code": 12, "kanji": "千葉県", "hira": "ちばけん", "kana": "チバケン", "roman": "CHIBA", "region": "関東"},  # noqa: E501
    13: {"code": 13, "kanji": "東京都", "hira": "とうきょうと", "kana": "トウキョウト", "roman": "TOKYO", "region": "関東"},  # noqa: E501
    14: {"code": 14, "kanji": "神奈川県", "hira": "かながわけん", "kana": "カナガワケン", "roman": "KANAGAWA", "region": "関東"},  # noqa: E501
    15: {"code": 15, "kanji": "新潟県", "hira": "にいがたけん", "kana": "ニイガタケン", "roman": "NIIGATA", "region": "中部"},  # noqa: E501
    16: {"code": 16, "kanji": "富山県", "hira": "とやまけん", "kana": "トヤマケン", "roman": "TOYAMA", "region": "中部"},  # noqa: E501
    17: {"code": 17, "kanji": "石川県", "hira": "いしかわけん", "kana": "イシカワケン", "roman": "ISHIKAWA", "region": "中部"},  # noqa: E501
    18: {"code": 18, "kanji": "福井県", "hira": "ふくいけん", "kana": "フクイケン", "roman": "FUKUI", "region": "中部"},  # noqa: E501
    19: {"code": 19, "kanji": "山梨県", "hira": "やまなしけん", "kana": "ヤマナシケン", "roman": "YAMANASHI", "region": "中部"},  # noqa: E501
    20: {"code": 20, "kanji": "長野県", "hira": "ながのけん", "kana": "ナガノケン", "roman": "NAGANO", "region": "中部"},  # noqa: E501
    21: {"code": 21, "kanji": "岐阜県", "hira": "ぎふけん", "kana": "ギフケン", "roman": "GIFU", "region": "中部"},  # noqa: E501
    22: {"code": 22, "kanji": "静岡県", "hira": "しずおかけん", "kana": "シズオカケン", "roman": "SHIZUOKA", "region": "中部"},  # noqa: E501
    23: {"code": 23, "kanji": "愛知県", "hira": "あいちけん", "kana": "アイチケン", "roman": "AICHI", "region": "中部"},  # noqa: E501
    24: {"code": 24, "kanji": "三重県", "hira": "みえけん", "kana": "ミエケン", "roman": "MIE", "region": "近畿"},  # noqa: E501
    25: {"code": 25, "kanji": "滋賀県", "hira": "しがけん", "kana": "シガケン", "roman": "SHIGA", "region": "近畿"},  # noqa: E501
    26: {"code": 26, "kanji": "京都府", "hira": "きょうとふ", "kana": "キョウトフ", "roman": "KYOTO", "region": "近畿"},  # noqa: E501
    27: {"code": 27, "kanji": "大阪府", "hira": "おおさかふ", "kana": "オオサカフ", "roman": "OSAKA", "region": "近畿"},  # noqa: E501
    28: {"code": 28, "kanji": "兵庫県", "hira": "ひょうごけん", "kana": "ヒョウゴケン", "roman": "HYOGO", "region": "近畿"},  # noqa: E501
    29: {"code": 29, "kanji": "奈良県", "hira": "ならけん", "kana": "ナラケン", "roman": "NARA", "region": "近畿"},  # noqa: E501
    30: {"code": 30, "kanji": "和歌山県", "hira": "わかやまけん", "kana": "ワカヤマケン", "roman": "WAKAYAMA", "region": "近畿"},  # noqa: E501
    31: {"code": 31, "kanji": "鳥取県", "hira": "とっとりけん", "kana": "トットリケン", "roman": "TOTTORI", "region": "中国"},  # noqa: E501
    32: {"code": 32, "kanji": "島根県", "hira": "しまねけん", "kana": "シマネケン", "roman": "SHIMANE", "region": "中国"},  # noqa: E501
    33: {"code": 33, "kanji": "岡山県", "hira": "おかやまけん", "kana": "オカヤマケン", "roman": "OKAYAMA", "region": "中国"},  # noqa: E501
    34: {"code": 34, "kanji": "広島県", "hira": "ひろしまけん", "kana": "ヒロシマケン", "roman": "HIROSHIMA", "region": "中国"},  # noqa: E501
    35: {"code": 35, "kanji": "山口県", "hira": "やまぐちけん", "kana": "ヤマグチケン", "roman": "YAMAGUCHI", "region": "中国"},  # noqa: E501
    36: {"code": 36, "kanji": "徳島県", "hira": "とくしまけん", "kana": "トクシマケン", "roman": "TOKUSHIMA", "region": "四国"},  # noqa: E501
    37: {"code": 37, "kanji": "香川県", "hira": "かがわけん", "kana": "カガワケン", "roman": "KAGAWA", "region": "四国"},  # noqa: E501
    38: {"code": 38, "kanji": "愛媛県", "hira": "えひめけん", "kana": "エヒメケン", "roman": "EHIME", "region": "四国"},  # noqa: E501
    39: {"code": 39, "kanji": "高知県", "hira": "こうちけん", "kana": "コウチケン", "roman": "KOCHI", "region": "四国"},  # noqa: E501
    40: {"code": 40, "kanji": "福岡県", "hira": "ふくおかけん", "kana": "フクオカケン", "roman": "FUKUOKA", "region": "九州・沖縄"},  # noqa: E501
    41: {"code": 41, "kanji": "佐賀県", "hira": "さがけん", "kana": "サガケン", "roman": "SAGA", "region": "九州・沖縄"},  # noqa: E501
    42: {"code": 42, "kanji": "長崎県", "hira": "ながさきけん", "kana": "ナガサキケン", "roman": "NAGASAKI", "region": "九州・沖縄"},  # noqa: E501
    43: {"code": 43, "kanji": "熊本県", "hira": "くまもとけん", "kana": "クマモトケン", "roman": "KUMAMOTO", "region": "九州・沖縄"},  # noqa: E501
    44: {"code": 44, "kanji": "大分県", "hira": "おおいたけん", "kana": "オオイタケン", "roman": "OITA", "region": "九州・沖縄"},  # noqa: E501
    45: {"code": 45, "kanji": "宮崎県", "hira": "みやざきけん", "kana": "ミヤザキケン", "roman": "MIYAZAKI", "region": "九州・沖縄"},  # noqa: E501
    46: {"code": 46, "kanji": "鹿児島県", "hira": "かごしまけん", "kana": "カゴシマケン", "roman": "KAGOSHIMA", "region": "九州・沖縄"},  # noqa: E501
    47: {"code": 47, "kanji": "沖縄県", "hira": "おきなわけん", "kana": "オキナワケン", "roman": "OKINAWA", "region": "九州・沖縄"},  # noqa: E501
}
# fmt: on

# 都道府県コードへ変換するためのマッピング
_ANY_TO_CODE_MAP: dict[str, int] = {}
for _code, _data in _PREFECTURE_DATA.items():
    # コード
    _ANY_TO_CODE_MAP[str(_code)] = _code

    # 漢字
    kanji_full = str(_data["kanji"])
    _ANY_TO_CODE_MAP[kanji_full] = _code
    if kanji_full == "北海道":
        pass
    if kanji_full.endswith("都") and kanji_full != "京都":
        _ANY_TO_CODE_MAP[kanji_full[:-1]] = _code
    elif kanji_full.endswith("府"):
        _ANY_TO_CODE_MAP[kanji_full[:-1]] = _code
    elif kanji_full.endswith("県"):
        _ANY_TO_CODE_MAP[kanji_full[:-1]] = _code

    # ひらがな
    hira_full = str(_data["hira"])
    _ANY_TO_CODE_MAP[hira_full] = _code
    if hira_full == "ほっかいどう":
        pass
    if hira_full.endswith("と") and hira_full != "きょうと":
        _ANY_TO_CODE_MAP[hira_full[:-1]] = _code
    elif hira_full.endswith("ふ"):
        _ANY_TO_CODE_MAP[hira_full[:-1]] = _code
    elif hira_full.endswith("けん"):
        _ANY_TO_CODE_MAP[hira_full[:-2]] = _code

    # カタカナ (全角大文字)
    kata_full = str(_data["kana"])
    _ANY_TO_CODE_MAP[kata_full] = _code
    if kata_full == "ホッカイドウ":
        pass
    if kata_full.endswith("ト") and kata_full != "キョウト":
        _ANY_TO_CODE_MAP[kata_full[:-1]] = _code
    elif kata_full.endswith("フ"):
        _ANY_TO_CODE_MAP[kata_full[:-1]] = _code
    elif kata_full.endswith("ケン"):
        _ANY_TO_CODE_MAP[kata_full[:-2]] = _code
    # ひらがなから変換したカタカナも登録 (小文字も含む)
    hira_for_kata = str(_data["hira"])

    # ローマ字 (大文字・小文字)
    _roman_full = str(_data["roman"]).upper()
    _ANY_TO_CODE_MAP[_roman_full] = _code
    _ANY_TO_CODE_MAP[_roman_full.lower()] = _code
    if _roman_full == "HOKKAIDO":
        pass
    elif _roman_full.endswith("TO") and _roman_full != "KYOTO":
        _ANY_TO_CODE_MAP[_roman_full[:-2]] = _code
        _ANY_TO_CODE_MAP[_roman_full[:-2].lower()] = _code
    elif _roman_full.endswith("FU"):
        _ANY_TO_CODE_MAP[_roman_full[:-2]] = _code
        _ANY_TO_CODE_MAP[_roman_full[:-2].lower()] = _code
    elif _roman_full.endswith("KEN"):
        _ANY_TO_CODE_MAP[_roman_full[:-3]] = _code
        _ANY_TO_CODE_MAP[_roman_full[:-3].lower()] = _code

# 茨城の特殊ケース
_ANY_TO_CODE_MAP["イバラギケン"] = 8
_ANY_TO_CODE_MAP["イバラギ"] = 8
_ANY_TO_CODE_MAP["いばらぎけん"] = 8
_ANY_TO_CODE_MAP["いばらぎ"] = 8


# 都道府県コードから漢字表記
_CODE_TO_KANJI_MAP: dict[int, str] = {
    code: str(data["kanji"]) for code, data in _PREFECTURE_DATA.items()
}
# 都道府県コードからひらがな表記
_CODE_TO_HIRAGANA_MAP: dict[int, str] = {
    code: str(data["hira"]) for code, data in _PREFECTURE_DATA.items()
}
# 都道府県コードからカタカナ表記
_CODE_TO_KATAKANA_MAP: dict[int, str] = {
    code: str(data["kana"]) for code, data in _PREFECTURE_DATA.items()
}
# 都道府県コードからローマ字表記
_CODE_TO_ROMAJI_MAP: dict[int, str] = {
    code: data["roman"] for code, data in _PREFECTURE_DATA.items()
}
# 都道府県コードから地方名
_CODE_TO_REGION_MAP: dict[int, str] = {
    code: str(data["region"]) for code, data in _PREFECTURE_DATA.items()
}


@register_expr_namespace("ja_pref")
class PrefectureExpr:
    def __init__(self, expr: pl.Expr):
        self._expr = expr

    def to_code(self) -> pl.Expr:
        """
        都道府県名（漢字、ひらがな、カタカナ、ローマ字、コード）を都道府県コードに変換します。
        表記揺れ（「県」の有無など）も吸収します。
        該当しない場合はnullになります。
        """
        normalized_expr = self._expr.cast(pl.Utf8).ja.normalize().str.to_uppercase()
        return normalized_expr.replace_strict(
            _ANY_TO_CODE_MAP, default=None, return_dtype=pl.Int64
        )

    def to_kanji(self) -> pl.Expr:
        """
        都道府県名またはコードを正式な漢字表記（例:「東京都」「神奈川県」）に変換します。
        入力が都道府県名の場合、まずコードに変換してから漢字表記にします。
        該当しない場合はnullになります。
        """
        code_expr = self.to_code()
        return code_expr.replace_strict(
            _CODE_TO_KANJI_MAP, default=None, return_dtype=pl.Utf8
        )

    def to_hiragana(self) -> pl.Expr:
        """
        都道府県名またはコードを正式なひらがな表記に変換します。
        該当しない場合はnullになります。
        """
        code_expr = self.to_code()
        return code_expr.replace_strict(
            _CODE_TO_HIRAGANA_MAP, default=None, return_dtype=pl.Utf8
        )

    def to_katakana(self) -> pl.Expr:
        """
        都道府県名またはコードを正式なカタカナ表記に変換します。
        該当しない場合はnullになります。
        """
        code_expr = self.to_code()
        return code_expr.replace_strict(
            _CODE_TO_KATAKANA_MAP, default=None, return_dtype=pl.Utf8
        )

    def to_romaji(self) -> pl.Expr:
        """
        都道府県名またはコードを一般的なローマ字表記に変換します。
        該当しない場合はnullになります。
        """
        code_expr = self.to_code()
        return code_expr.replace_strict(
            _CODE_TO_ROMAJI_MAP, default=None, return_dtype=pl.Utf8
        )

    def to_region(self) -> pl.Expr:
        """
        都道府県名またはコードを地方名（北海道、東北、関東など）に変換します。
        該当しない場合はnullになります。
        """
        code_expr = self.to_code()
        return code_expr.replace_strict(
            _CODE_TO_REGION_MAP, default=None, return_dtype=pl.Utf8
        )
