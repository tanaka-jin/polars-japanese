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
            pl.Expr: 祝日の場合は True、そうでない場合は False を含む
                Boolean エクスプレッション。
        """
        return self._expr.map_elements(
            lambda x: jpholiday.is_holiday(x) if isinstance(x, date) else None,
            return_dtype=pl.Boolean,
            skip_nulls=False,
        )

    def is_business_day(self) -> pl.Expr:
        """
        指定された日付が営業日かどうかを判定します。
        (土日祝日でない場合に True)

        Returns:
            pl.Expr: 営業日の場合は True、そうでない場合は False を含む
                Boolean エクスプレッション。
        """
        return self._expr.map_elements(
            lambda x: isinstance(x, date)
            and not jpholiday.is_holiday(x)
            and x.weekday() < 5  # 土日(5,6)を除外
            if isinstance(x, date)
            else None,
            return_dtype=pl.Boolean,
            skip_nulls=False,
        )
