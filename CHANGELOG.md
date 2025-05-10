# 更新履歴

## [Unreleased]
### Added
- 都道府県名と都道府県コードの相互変換機能を追加 (`ja_pref.to_code`, `ja_pref.to_kanji`, `ja_pref.to_hiragana`, `ja_pref.to_katakana`, `ja_pref.to_romaji`)
- 都道府県コードから地方名（北海道、東北など）への変換機能を追加 (`ja_pref.to_region`)
- `Expr.ja.to_weekday_name(format: str = "%A")` を追加し、Date/Datetimeを日本語の曜日文字列に変換できるようにしました。`"%A"`（例: "月曜日"）と`"%a"`（例: "月"）のフォーマットをサポートします。

### Fixed
- `to_csv` を `write_csv` に変更

## [0.1.2] - 2024-05-05
### Fixed
- WindowsでのBuildを修正

## [0.1.1] - 2024-05-04
### Fixed
- plugin Importのエラーを修正

## [0.1.0] - 2024-05-04

### Added
- polars-japaneseの初回リリース
- Polars DataFrameに日本語特有の機能を追加:
  - 半角/全角文字変換 (`to_full_width`, `to_half_width`)
  - 漢数字変換 (`convert_numbers`, `to_kanji`)
  - 和暦/西暦変換 (`to_era`, `from_era`)
  - 日本の祝日判定 (`is_holiday`, `is_businessday`)
  - CSVファイルの文字エンコーディング指定による読み書き
  - 文字列の正規化 (NFKC準拠)
