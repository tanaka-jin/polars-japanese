from pathlib import Path

import polars as pl
from polars._typing import IntoExpr
from polars.plugins import register_plugin_function

PLUGIN_PATH = Path(__file__).parent.parent


def to_half_width(expr: IntoExpr) -> pl.Expr:
    return register_plugin_function(
        plugin_path=PLUGIN_PATH,
        function_name="to_half_width",
        args=expr,
        is_elementwise=True,
    )


def to_full_width(expr: IntoExpr) -> pl.Expr:
    return register_plugin_function(
        plugin_path=PLUGIN_PATH,
        function_name="to_full_width",
        args=expr,
        is_elementwise=True,
    )
