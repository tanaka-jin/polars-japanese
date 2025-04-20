import pathlib
from typing import Optional, Union

import kanjize
import polars as pl
from polars.api import register_dataframe_namespace, register_expr_namespace

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
        表現の文字列出力に含まれる全角文字を半角に変換します。
        カタカナ、ASCII、数字に適用されます。
        """
        return JaconvExpr(self._expr).to_half_width()

    def to_full_width(self) -> pl.Expr:
        """
        表現の文字列出力に含まれる半角文字を全角に変換します。
        カタカナ、ASCII、数字に適用されます。
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
        表現のDateまたはDatetime出力を和暦（日本の元号）の
        文字列形式に変換します。
        """
        return JapaneraExpr(self._expr).to_wareki(
            format=format, raise_error=raise_error
        )

    def to_kanji(
        self, config: Optional[kanjize.KanjizeConfiguration] = None
    ) -> pl.Expr:
        """
        表現のInt出力を漢字（日本の数字）の
        文字列形式に変換します。
        """
        return KanjizeExpr(self._expr).to_kanji(config=config)

    def to_number(self) -> pl.Expr:
        """
        漢字（日本の数字）の表現の文字列出力を数値に変換します。
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


@register_dataframe_namespace("ja")
class JapaneseDataFrame:
    def __init__(self, df: pl.DataFrame):
        self._df = df

    def to_csv(
        self,
        path: Union[str, pathlib.Path],
        encoding: str = "utf-8",
        **kwargs,
    ) -> None:
        """
        指定されたエンコーディングでDataFrameをCSVファイルに書き込みます。

        Parameters
        ----------
        path : Union[str, pathlib.Path]
            CSVファイルを書き込むパス。
        encoding : str, default "utf-8"
            出力ファイルに使用するエンコーディング。
        **kwargs
            `polars.DataFrame.write_csv` に渡される追加のキーワード引数。

        Examples
        --------
        >>> import polars as pl
        >>> import polars_japanese # noqa: F401
        >>> df = pl.DataFrame({"col1": ["テスト", "データ"], "col2": [1, 2]})
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
