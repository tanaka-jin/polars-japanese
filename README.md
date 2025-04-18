# polars-japanese: Polars 日本語拡張ライブラリ (Polars Japanese Extension Library)

[![PyPI version](https://badge.fury.io/py/polars-japanese.svg)](https://badge.fury.io/py/polars-japanese)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Polars DataFrame/Expression API に、日本語処理や日本固有の操作に関連する機能を追加する拡張ライブラリです。

(This is an extension library that adds functionalities related to Japanese text processing and Japan-specific operations to the Polars DataFrame/Expression API.)

## 概要 (Overview)

`polars-japanese` は、データ分析ライブラリ [Polars](https://pola.rs/) の強力な機能を活用しつつ、日本語特有のデータ処理（全角/半角変換、漢数字変換、和暦変換、祝日判定など）を容易に行えるように設計されています。 Polars の Expression API を拡張し、`.ja` アクセサを通じて直感的にこれらの機能を利用できます。

## 主な機能 (Features)

*   **全角/半角変換 (Full-width/Half-width Conversion):** 文字列の全角と半角を相互に変換します (Powered by [jaconv](https://github.com/ikegami-yukino/jaconv))。
    *   `to_half_width()`: 全角文字を半角文字に変換します
    *   `to_full_width()`: 半角文字を全角文字に変換します
    *   `normalize()`: 全角/半角文字を統一的に正規化します
*   **漢数字変換 (Kanji Numeral Conversion):** 文字列中の漢数字をアラビア数字に変換します (Powered by [kanjize](https://github.com/takavfx/kanjize))。
    *   `to_number()`: 漢数字（例: "千二百三十四"）を整数（例: 1234）に変換します
*   **和暦/西暦変換 (Japanese Era/Western Calendar Conversion):** 和暦文字列と西暦日付/文字列を相互に変換します (Powered by [japanera](https://github.com/osaka-u/japanera))。
    *   `to_wareki()`: 西暦日付/文字列を和暦文字列（例: "令和六年"）に変換します
    *   `to_datetime()`: 和暦文字列を西暦日付に変換します
*   **祝日判定 (Holiday Determination):** 指定された日付が日本の祝日かどうかを判定します (Powered by [jpholiday](https://github.com/jpholiday/jpholiday))。
    *   `is_holiday()`: 日付が祝日であれば `True` を返します

## インストール (Installation)

```bash
pip install git+https://github.com/tanaka-jin/polars-japanese
```

## 使い方 (Usage)

`polars-japanese` をインポートすると、Polars の Expression API に `.ja` アクセサが追加されます。


```python
import polars as pl
import polars_japanese
from datetime import date

df = pl.DataFrame({
    "text_zen": ["Ｐｏｌａｒｓ", "ﾃﾞｰﾀﾌﾚｰﾑ", "１２３"],
    "text_han": ["Polars", "ﾃﾞｰﾀﾌﾚｰﾑ", "123"],
    "kanji_num": ["千二百三十四", "五十六", None],
    "wareki_str": ["令和六年", "平成元年", "昭和四十五年"],
    "seireki_date": [date(2024, 4, 18), date(1989, 1, 8), date(1970, 10, 10)],
})

# 全角/半角変換
df = df.with_columns(
    pl.col("text_zen").ja.to_half_width().alias("to_half"),
    pl.col("text_han").ja.to_full_width().alias("to_full"),
    pl.col("text_zen").ja.normalize().alias("normalized"),
)

# 漢数字変換
df = df.with_columns(
    pl.col("kanji_num").ja.to_number().alias("num_from_kanji")
)

# 和暦/西暦変換
df = df.with_columns(
    pl.col("seireki_date").ja.to_wareki().alias("wareki_from_seireki"),
    pl.col("wareki_str").ja.to_datetime().alias("seireki_from_wareki"),
)

# 祝日判定
df = df.with_columns(
    pl.col("seireki_date").ja.is_holiday().alias("is_holiday"),
)

print(df)
```

## ライセンス (License)

このプロジェクトは MIT ライセンスの下で公開されています。詳細は `LICENSE` ファイルをご覧ください。

## 作者 (Author)

*   Jin Tanaka ([@tanaka-jin](https://github.com/tanaka-jin))
