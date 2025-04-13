from datetime import date

import jpholiday
import polars as pl


class JpholidayExpr:
    """
    polarsでjpholidayを利用するためのExpression拡張
    """

    def __init__(self, expr: pl.Expr):
        self._expr = expr

    def is_holiday(self) -> pl.Expr:
        """
        指定された日付が祝日かどうかを判定します。

        Returns:
            pl.Expr: 祝日の場合はTrue、そうでない場合はFalse。
        """
        return self._expr.map_elements(
            lambda x: jpholiday.is_holiday(x) if isinstance(x, date) else None,
            return_dtype=pl.Boolean,
            skip_nulls=False,
        )

    def is_business_day(self) -> pl.Expr:
        """
        指定された日付が営業日かどうかを判定します。

        Returns:
            pl.Expr: 営業日の場合はTrue、そうでない場合はFalse。
        """
        return self._expr.map_elements(
            lambda x: not jpholiday.is_holiday(x)
            if isinstance(x, date)
            else None,
            return_dtype=pl.Boolean,
            skip_nulls=False,
        )
