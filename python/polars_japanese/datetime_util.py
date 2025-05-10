import polars as pl

# 日本語の曜日マッピング
_JAPANESE_WEEKDAYS_FULL = {
    1: "月曜日",
    2: "火曜日",
    3: "水曜日",
    4: "木曜日",
    5: "金曜日",
    6: "土曜日",
    7: "日曜日",
}
_JAPANESE_WEEKDAYS_SHORT = {
    1: "月",
    2: "火",
    3: "水",
    4: "木",
    5: "金",
    6: "土",
    7: "日",
}


class DatetimeUtilityExpr:
    def __init__(self, expr: pl.Expr):
        self._expr = expr

    def to_weekday_name(self, format: str = "%A") -> pl.Expr:
        """
        Date型またはDatetime型のエクスプレッションを日本語の曜日文字列に変換します。

        入力データがNoneの場合はNoneを返します。

        Args:
            format (str, optional): 出力フォーマット。
                "%A" (デフォルト): "月曜日", "火曜日", ...
                "%a": "月", "火", ...

        Returns:
            pl.Expr: 日本語の曜日文字列を含むエクスプレッション。

        Raises:
            ValueError: サポートされていないフォーマットが指定された場合。
        """
        if format == "%A":
            mapping = _JAPANESE_WEEKDAYS_FULL
        elif format == "%a":
            mapping = _JAPANESE_WEEKDAYS_SHORT
        else:
            raise ValueError(
                f"Unsupported format string: {format}. Supported formats: '%A', '%a'."
            )

        return (
            self._expr.dt.weekday()
            .replace_strict(mapping, default=None)
            .cast(pl.String)
        )

    # 将来的なJST変換メソッドのプレースホルダー
    # def to_jst(self) -> pl.Expr:
    #     """
    #     Datetime型のエクスプレッションを日本標準時(JST, UTC+9)に変換します。
    #     入力がnaive datetimeの場合はUTCとみなします。
    #     """
    #     # 実装は別途
    #     pass
