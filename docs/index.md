# polars-japanese: Polars 日本語拡張ライブラリ (Polars Japanese Extension Library)

[![PyPI version](https://badge.fury.io/py/polars-japanese.svg)](https://badge.fury.io/py/polars-japanese)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Polars DataFrame/Expression API に、日本語処理や日本固有の操作に関連する機能を追加する拡張ライブラリです。

(This is an extension library that adds functionalities related to Japanese text processing and Japan-specific operations to the Polars DataFrame/Expression API.)

## 概要 (Overview)

`polars-japanese` は、データ分析ライブラリ [Polars](https://pola.rs/) の強力な機能を活用しつつ、日本語特有のデータ処理（全角/半角変換、漢数字変換、和暦変換、祝日判定など）を容易に行えるように設計されています。 Polars の Expression API を拡張し、`.ja` アクセサを通じて直感的にこれらの機能を利用できます。


## インストール (Installation)

```bash
pip install polars-japanese
```

## 使い方 (Usage)

`polars-japanese` をインポートすると、Polars の Expression API に `.ja` アクセサが追加されます。


```python
import polars as pl
import polars_japanese
from datetime import date

df = pl.DataFrame({
    "kanji_num": ["千二百三十四", "五十六", None],
    "wareki_str": ["令和6年1月1日", "平成1年12月31日", "昭和45年12月04日"],
    "seireki_date": [date(2024, 4, 18), date(1989, 1, 8), date(1970, 10, 10)],
    "text_zen": ["Ｐｏｌａｒｓ", "データ", "１２３"],
})

df = df.select(
    # 漢数字変換
    pl.col("kanji_num").ja.to_number().alias("num_from_kanji"),
    # 和暦/西暦変換
    pl.col("wareki_str").ja.to_datetime().alias("seireki_from_wareki"),
    # 祝日判定
    pl.col("seireki_date").ja.is_holiday().alias("is_holiday"),
    # 全角/半角変換
    pl.col("text_zen").ja.to_half_width().alias("to_half"),
    pl.col("text_zen").ja.normalize().alias("normalized"),
)

print(df)

# ┌────────────────┬─────────────────────┬────────────┬─────────┬────────────┐
# │ num_from_kanji ┆ seireki_from_wareki ┆ is_holiday ┆ to_half ┆ normalized │
# │ ---            ┆ ---                 ┆ ---        ┆ ---     ┆ ---        │
# │ i64            ┆ date                ┆ bool       ┆ str     ┆ str        │
# ╞════════════════╪═════════════════════╪════════════╪═════════╪════════════╡
# │ 1234           ┆ 2024-01-01          ┆ false      ┆ Polars  ┆ Polars     │
# │ 56             ┆ 1989-12-31          ┆ false      ┆ ﾃﾞｰﾀ     ┆ データ     │
# │ null           ┆ 1970-12-04          ┆ true       ┆ 123     ┆ 123        │
# └────────────────┴─────────────────────┴────────────┴─────────┴────────────┘

df.ja.to_csv("output_sjis.csv", encoding="shift_jis")
```

## 主な機能 (Features)

*   **全角/半角変換:** 文字列の全角と半角を相互に変換します (Rust plugin)。
    *   `to_half_width()`: 全角文字を半角文字に変換します
    *   `to_full_width()`: 半角文字を全角文字に変換します
    *   `normalize()`: 全角/半角文字を統一的に正規化します。Unicode NFKC形式で正規化します。
*   **漢数字変換:** 文字列中の漢数字をアラビア数字に変換します (Powered by [kanjize](https://github.com/takavfx/kanjize))。
    *   `to_number()`: 漢数字（例: "千二百三十四"）を整数（例: 1234）に変換します
    *   `to_kanji()`: 数値を漢数字に変換します。`config`引数で`KanjizeConfiguration`を指定できます。
*   **和暦/西暦変換:** 和暦文字列と西暦日付/文字列を相互に変換します (Powered by [japanera](https://github.com/osaka-u/japanera))。
    *   `to_wareki()`: 西暦日付/文字列を和暦文字列（例: "令和6年10月10日"）に変換します。`format`引数で出力フォーマットを指定できます。`raise_error`引数でエラー発生時の挙動を制御できます。
    *   `to_datetime()`: 和暦文字列を西暦日付に変換します。`format`引数で入力フォーマットを指定できます。`raise_error`引数でエラー発生時の挙動を制御できます。
*   **祝日判定:** 指定された日付が日本の祝日かどうかを判定します (Powered by [jpholiday](https://github.com/jpholiday/jpholiday))。
    *   `is_holiday()`: 日付が祝日であれば `True` を返します
    *   `is_business_day()`: 日付が営業日であれば `True` を返します
*   **CSVエンコーディング指定出力:** DataFrameを指定したエンコーディングでCSVファイルに出力します。
    *   `DataFrame.ja.to_csv(path, encoding="shift_jis", **kwargs)`: DataFrameをCSVファイルに書き込みます。
