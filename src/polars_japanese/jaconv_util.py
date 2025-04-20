import jaconv
import polars as pl


class JaconvExpr:
    def __init__(self, expr: pl.Expr):
        self._expr = expr

    def to_half_width(self) -> pl.Expr:
        """
        表現の文字列出力に含まれる全角文字を半角に変換します。
        カタカナ、ASCII、数字に適用されます。
        """
        return self._expr.map_elements(
            lambda x: jaconv.z2h(x, kana=True, ascii=True, digit=True)
            if x is not None
            else None,
            return_dtype=pl.Utf8,
            skip_nulls=False,
        )

    def to_full_width(self) -> pl.Expr:
        """
        表現の文字列出力に含まれる半角文字を全角に変換します。
        カタカナ、ASCII、数字に適用されます。
        """
        return self._expr.map_elements(
            lambda x: jaconv.h2z(x, kana=True, ascii=True, digit=True)
            if x is not None
            else None,
            return_dtype=pl.Utf8,
            skip_nulls=False,
        )

    def normalize(self) -> pl.Expr:
        """
        正規化処理
        """
        return self._expr.map_elements(
            lambda x: jaconv.normalize(x) if x is not None else None,
            return_dtype=pl.Utf8,
            skip_nulls=False,
        )
