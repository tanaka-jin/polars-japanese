import datetime as dt
from typing import Optional

import polars as pl
from japanera import EraDate


class JapaneraExpr:
    def __init__(self, expr: pl.Expr):
        self._expr = expr

    def to_wareki(
        self,
        format: str = "%-K%-y年%m月%d日",
        raise_error: bool = True,
    ) -> pl.Expr:
        """
        Polars の Date 型を和暦文字列に変換します。

        Args:
            format (str, optional): 出力する和暦のフォーマット文字列。
                デフォルトは "%-K%-y年%m月%d日"。
            raise_error (bool, optional):
                変換エラー時に例外を発生させるかどうか。デフォルトは True。

        Returns:
            pl.Expr: 和暦文字列に変換されたエクスプレッション。
        """

        def _to_wareki(
            x: dt.date,
            format: str = "%-K%-y年%m月%d日",
            raise_error: bool = True,
        ) -> Optional[str]:
            if x is None:
                return None
            try:
                # strftime の呼び出しをインスタンスメソッドに戻す
                era_date_obj = EraDate.from_date(x)
                return era_date_obj.strftime(format)
            except ValueError:
                if raise_error:
                    raise
                else:
                    return None

        return self._expr.map_elements(
            lambda x: _to_wareki(x, format, raise_error),
            return_dtype=pl.Utf8,
            skip_nulls=False,
        )

    def to_datetime(
        self, format: str = "%-K%-y年%m月%d日", raise_error: bool = True
    ) -> pl.Expr:
        """
        和暦文字列を Polars の Date 型に変換します。

        Args:
            format (str, optional): 和暦のフォーマット文字列。
                デフォルトは "%-K%-y年%m月%d日"。
            raise_error (bool, optional):
                変換エラー時に例外を発生させるかどうか。デフォルトは True。

        Returns:
            pl.Expr: Date 型に変換されたエクスプレッション。
        """

        def _to_datetime(
            x: str, format: str = "%-K%-y年%m月%d日", raise_error: bool = True
        ) -> Optional[dt.date]:
            if x is None:
                return None
            try:
                # strptime のフォーマット文字列を %g%e に戻す
                era_dates = EraDate.strptime(x, format)
                if era_dates:
                    return era_dates[0].to_date()
                else:
                    return None
            except ValueError:
                if raise_error:
                    raise
                else:
                    return None

        return self._expr.map_elements(
            lambda x: _to_datetime(x, format, raise_error),
            return_dtype=pl.Date,
            skip_nulls=False,
        )
