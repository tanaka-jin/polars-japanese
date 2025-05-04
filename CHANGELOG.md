# Changelog

## [Unreleased]

### Added
- Added `DataFrame.ja.to_csv` method to write DataFrame to CSV with specified encoding.

### Changed
- Modified `Expr.ja.normalize` to use a Python implementation based on NFKC normalization and custom rules (e.g., unifying hyphens, tildes, spaces), removing the `jaconv` dependency for this specific function.

### Fixed
- Fixed a bug in `is_businessday` function.

## [0.1.0] - 2024-04-18

### Added
- Initial release of polars-japanese.
- Provides Japanese-specific functionalities for Polars DataFrames, including:
  - Full-width/half-width character conversion
  - Kanji numeral conversion
  - Japanese Era/Western calendar conversion
  - Holiday determination
