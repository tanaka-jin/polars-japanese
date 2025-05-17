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

    def to_jst(self, time_zone: str | None = None) -> pl.Expr:
        """
        Datetime型のエクスプレッションを日本標準時(JST, UTC+9)に変換します。

        Args:
            time_zone (str | None, optional): 入力データのタイムゾーン。
                Noneの場合、naive datetimeはUTCとみなされます。
                タイムゾーンが指定された場合、入力データはそのタイムゾーンとして解釈されます。

        Returns:
            pl.Expr: 日本標準時(JST)に変換されたDatetime型のエクスプレッション。
        """
        if time_zone:
            # 指定されたタイムゾーンとして解釈し、JSTに変換
            return self._expr.dt.replace_time_zone(time_zone).dt.convert_time_zone(
                "Asia/Tokyo"
            )
        else:
            # naive datetimeはUTCとみなしてJSTに変換
            return self._expr.cast(pl.Datetime()).dt.convert_time_zone("Asia/Tokyo")
