# 更新履歴

## [Unreleased]
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

