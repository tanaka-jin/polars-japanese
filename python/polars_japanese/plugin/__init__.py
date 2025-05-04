import sys
from pathlib import Path

import polars as pl
from polars._typing import IntoExpr
from polars.plugins import register_plugin_function

# Rust でビルドされた .so ファイルへのパスを計算
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
TARGET_DIR = PROJECT_ROOT / "target" / "release"

# OSに応じてライブラリの拡張子を決定
if sys.platform == "win32":
    LIB_NAME = "polars_japanese.dll"
elif sys.platform == "darwin":
    LIB_NAME = "libpolars_japanese.dylib"
else:
    LIB_NAME = "libpolars_japanese.so"

PLUGIN_PATH = TARGET_DIR / LIB_NAME

# 開発モードでは target/release に .so があることを期待
# 本番パッケージング時は maturin が適切に配置するはず
# if not PLUGIN_PATH.exists():
#     # ここでエラーを出すか、別のパスを探すか検討
#     # 例: raise ImportError(f"Plugin library not found at {PLUGIN_PATH}")
#     pass


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
