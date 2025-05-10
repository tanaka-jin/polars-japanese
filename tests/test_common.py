import pathlib

import polars as pl
import polars_japanese  # noqa: F401
import pytest
from polars.testing import assert_frame_equal


def test_write_csv_encoding_sjis(tmp_path: pathlib.Path) -> None:
    """Shift-JISエンコーディングでCSVファイルが出力されることをテストする"""
    df = pl.DataFrame({"col1": ["テスト", "データ"], "col2": [1, 2]})
    output_path = tmp_path / "test_sjis.csv"

    # ja名前空間経由でwrite_csvを呼び出す
    df.ja.write_csv(output_path, encoding="shift_jis")

    # 出力されたファイルをShift-JISで読み込み、内容を確認する
    with open(output_path, "r", encoding="shift_jis") as f:
        content = f.read()
        expected_content = "col1,col2\nテスト,1\nデータ,2\n"
        assert content == expected_content

    # Polarsで読み込んでDataFrameが一致することも確認
    read_df = pl.read_csv(output_path, encoding="shift_jis")
    assert_frame_equal(df, read_df)


def test_write_csv_encoding_utf8(tmp_path: pathlib.Path) -> None:
    """UTF-8エンコーディングでCSVファイルが出力されることをテストする"""
    df = pl.DataFrame({"col1": ["テスト", "データ"], "col2": [1, 2]})
    output_path = tmp_path / "test_utf8.csv"

    # ja名前空間経由でwrite_csvを呼び出す
    df.ja.write_csv(output_path, encoding="utf-8")

    # 出力されたファイルをUTF-8で読み込み、内容を確認する
    with open(output_path, "r", encoding="utf-8") as f:
        content = f.read()
        expected_content = "col1,col2\nテスト,1\nデータ,2\n"
        assert content == expected_content

    # Polarsで読み込んでDataFrameが一致することも確認
    read_df = pl.read_csv(output_path, encoding="utf-8")
    assert_frame_equal(df, read_df)


def test_write_csv_encoding_unsupported(tmp_path: pathlib.Path) -> None:
    """サポートされていないエンコーディングを指定した場合にエラーが発生することをテストする"""
    df = pl.DataFrame({"col1": ["テスト", "データ"], "col2": [1, 2]})
    output_path = tmp_path / "test_unsupported.csv"

    with pytest.raises(LookupError):
        # ja名前空間経由でwrite_csvを呼び出す
        df.ja.write_csv(output_path, encoding="unsupported_encoding")
