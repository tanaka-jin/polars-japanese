from typing import Optional

import kanjize
import polars as pl


class KanjizeExpr:
    def __init__(self, expr: pl.Expr):
        self._expr = expr

    def to_kanji(
        self, config: Optional[kanjize.KanjizeConfiguration] = None
    ) -> pl.Expr:
        """
        数値を漢数字に変換します。

        Args:
            config (Optional[kanjize.KanjizeConfiguration], optional):
                kanjize の設定。デフォルトは None。

        Returns:
            pl.Expr: 漢数字文字列に変換されたエクスプレッション。
        """
        return self._expr.map_elements(
            lambda x: kanjize.number2kanji(x, config=config)
            if x is not None
            else None,
            return_dtype=pl.Utf8,
            skip_nulls=False,
        )

    def to_number(self) -> pl.Expr:
        """
        漢数字を数値に変換します。

        Returns:
            pl.Expr: 数値に変換されたエクスプレッション (Int64)。
        """
        return self._expr.map_elements(
            lambda x: kanjize.kanji2number(x) if x is not None else None,
            return_dtype=pl.Int64,
            skip_nulls=False,
        )
