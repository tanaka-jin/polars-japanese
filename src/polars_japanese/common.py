import pathlib
from typing import Any, Optional, Union

import kanjize
import polars as pl
from polars.api import register_dataframe_namespace, register_expr_namespace

from polars_japanese.plugin import to_full_width, to_half_width

# from .jaconv_util import JaconvExpr
from .japanera_util import JapaneraExpr
from .jpholiday_util import JpholidayExpr
from .kanjize_util import KanjizeExpr
from .normalize_util import NormalizeExpr


@register_expr_namespace("ja")
class JapaneseExpr:
    def __init__(self, expr: pl.Expr):
        self._expr = expr

    def to_half_width(self) -> pl.Expr:
        """
        エクスプレッションの文字列に含まれる全角文字を半角に変換します。
        カタカナ、ASCII、数字に適用されます。

        Returns:
            pl.Expr: 半角に変換された文字列を含むエクスプレッション。
        """
        return to_half_width(self._expr)

    def to_full_width(self) -> pl.Expr:
        """
        エクスプレッションの文字列に含まれる半角文字を全角に変換します。
        カタカナ、ASCII、数字に適用されます。

        Returns:
            pl.Expr: 全角に変換された文字列を含むエクスプレッション。
        """
        return to_full_width(self._expr)

    def normalize(self) -> pl.Expr:
        """
        エクスプレッションの文字列を正規化します。

        Unicode正規化 (NFKC) を適用した後、以下の日本語特有のルールを適用:
        - ハイフン/マイナス記号 (`‐`, `－` など) を半角ハイフン (`-`) に統一。
        - チルダ (`~`) を全角チルダ (`～`) に統一。
        - 感嘆符 (`！`) を半角 (`!`) に統一。
        - 疑問符 (`？`) を半角 (`?`) に統一。
        - 全角スペース (`　`) を半角スペース (` `) に変換し、
          連続する空白文字を単一の半角スペースにまとめ、先頭と末尾の空白を削除。

        Returns:
            pl.Expr: 正規化された文字列を含むエクスプレッション。
        """
        # Use the new Python-based implementation
        return NormalizeExpr(self._expr).normalize()

    def to_datetime(
        self, format: str = "%-K%-y年%m月%d日", raise_error: bool = True
    ) -> pl.Expr:
        """
        和暦文字列を Polars の Date 型に変換します。

        Args:
            format (str, optional): 和暦のフォーマット文字列。
            raise_error (bool, optional):
                変換エラー時に例外を発生させるかどうか。

        Returns:
            pl.Expr: Date 型に変換されたエクスプレッション。

        References:
            <https://japanera.readthedocs.io/en/latest/>
        """
        return JapaneraExpr(self._expr).to_datetime(
            format=format, raise_error=raise_error
        )

    def to_wareki(
        self,
        format: str = "%-K%-Y年%m月%d日",
        raise_error: bool = True,
    ) -> pl.Expr:
        """
        エクスプレッションのDateまたはDatetimeを和暦の文字列形式に変換します。

        Args:
            format (str, optional): 出力する和暦のフォーマット文字列。
            raise_error (bool, optional):
                変換エラー時に例外を発生させるかどうか。

        Returns:
            pl.Expr: 和暦文字列に変換されたエクスプレッション。

        References:
            <https://japanera.readthedocs.io/en/latest/>
        """
        return JapaneraExpr(self._expr).to_wareki(
            format=format, raise_error=raise_error
        )

    def to_kanji(
        self, config: Optional[kanjize.KanjizeConfiguration] = None
    ) -> pl.Expr:
        """
        エクスプレッションのIntを漢数字の文字列形式に変換します。

        Args:
            config (Optional[kanjize.KanjizeConfiguration], optional):
                kanjize の設定。

        Returns:
            pl.Expr: 漢数字文字列に変換されたエクスプレッション。

        References:
            <https://github.com/nagataaaas/kanjize>
        """
        return KanjizeExpr(self._expr).to_kanji(config=config)

    def to_number(self) -> pl.Expr:
        """
        エクスプレッションの漢数字を数値に変換します。

        Returns:
            pl.Expr: 数値に変換されたエクスプレッション (Int64)。

        References:
            <https://github.com/nagataaaas/kanjize>
        """
        return KanjizeExpr(self._expr).to_number()

    def is_holiday(self) -> pl.Expr:
        """
        指定された日付が祝日かどうかを判定します。

        Returns:
            pl.Expr: 祝日の場合は True、そうでない場合は False を含む
                Boolean エクスプレッション。
        """
        return JpholidayExpr(self._expr).is_holiday()

    def is_business_day(self) -> pl.Expr:
        """
        指定された日付が営業日かどうかを判定します。
        (土日祝日でない場合に True)

        Returns:
            pl.Expr: 営業日の場合は True、そうでない場合は False を含む
                Boolean エクスプレッション。
        """
        return JpholidayExpr(self._expr).is_business_day()


@register_dataframe_namespace("ja")
class JapaneseDataFrame:
    def __init__(self, df: pl.DataFrame):
        self._df = df

    def to_csv(
        self,
        path: Union[str, pathlib.Path],
        encoding: str = "utf-8",
        **kwargs: Any,
    ) -> None:
        """
        指定されたエンコーディングでDataFrameをCSVファイルに書き込みます。

        Args:
            path (Union[str, pathlib.Path]): CSVファイルを書き込むパス。
            encoding (str, optional): 出力ファイルに使用するエンコーディング。
                デフォルトは "utf-8"。
            **kwargs: `polars.DataFrame.write_csv` に
                渡される追加のキーワード引数。

        Raises:
            LookupError: 指定されたエンコーディングが無効な場合に発生します。

        Examples:
            >>> import polars as pl
            >>> import polars_japanese # noqa: F401
            >>> df = pl.DataFrame({"col1": ["テスト", "一"], "col2": [1, 2]})
            >>> # Shift-JISエンコーディングでCSVに書き込む
            >>> # df.ja.to_csv("output.csv", encoding="shift_jis")
        """
        try:
            # ファイルを開く前にエンコーディングが有効か確認
            "".encode(encoding)
        except LookupError:
            raise LookupError(f"不明なエンコーディングです: {encoding}")

        csv_string = self._df.write_csv(**kwargs)
        with open(path, "w", encoding=encoding) as fw:
            fw.write(csv_string)
