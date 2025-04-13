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
        Convert a number to kanji (Japanese numeral).
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
        Convert kanji (Japanese numeral) to a number.
        """
        return self._expr.map_elements(
            lambda x: kanjize.kanji2number(x) if x is not None else None,
            return_dtype=pl.Int64,
            skip_nulls=False,
        )
