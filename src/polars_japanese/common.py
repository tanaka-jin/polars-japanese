from typing import Optional

import kanjize
import polars as pl
from polars.api import register_expr_namespace

from .jaconv_util import JaconvExpr
from .japanera_util import JapaneraExpr
from .jpholiday_util import JpholidayExpr
from .kanjize_util import KanjizeExpr


@register_expr_namespace("ja")
class JapaneseExpr:
    def __init__(self, expr: pl.Expr):
        self._expr = expr

    def to_half_width(self) -> pl.Expr:
        """
        Convert full-width characters in the expression's string output
        to half-width. Applies to Katakana, ASCII, and digits.
        """
        return JaconvExpr(self._expr).to_half_width()

    def to_full_width(self) -> pl.Expr:
        """
        Convert half-width characters in the expression's string output
        to full-width. Applies to Katakana, ASCII, and digits.
        """
        return JaconvExpr(self._expr).to_full_width()

    def normalize(self) -> pl.Expr:
        """
        正規化処理
        """
        return JaconvExpr(self._expr).normalize()

    def to_datetime(
        self, format: str = "%-K%-y年%m月%d日", raise_error: bool = True
    ) -> pl.Expr:
        """
        和暦文字列を Polars の Date 型に変換します。
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
        Convert the expression's Date or Datetime output to Wareki
        (Japanese era)
        string representation.
        """
        return JapaneraExpr(self._expr).to_wareki(
            format=format, raise_error=raise_error
        )

    def to_kanji(
        self, config: Optional[kanjize.KanjizeConfiguration] = None
    ) -> pl.Expr:
        """
        Convert the expression's Int output to Kanji (Japanese numeral)
        string representation.
        """
        return KanjizeExpr(self._expr).to_kanji(config=config)

    def to_number(self) -> pl.Expr:
        """
        Convert the expression's string output of Kanji (Japanese numeral)
        to number.
        """
        return KanjizeExpr(self._expr).to_number()

    def is_holiday(self) -> pl.Expr:
        """
        指定された日付が祝日かどうかを判定します。
        """
        return JpholidayExpr(self._expr).is_holiday()

    def is_business_day(self) -> pl.Expr:
        """
        指定された日付が営業日かどうかを判定します。
        """
        return JpholidayExpr(self._expr).is_business_day()
