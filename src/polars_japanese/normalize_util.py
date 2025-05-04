import polars as pl


class NormalizeExpr:
    """
    日本語テキスト正規化のためのPolars Expression

    このクラスは、NFKCによる正規化と特定の日本語文字の置換に基づいて、
    Polars expressions内で日本語テキストを正規化するメソッドを提供します。
    """

    def __init__(self, expr: pl.Expr):
        self._expr = expr

    def normalize(self) -> pl.Expr:
        """
        式内の日本語テキストを正規化します。

        まずNFKC正規化を適用し、その後以下の特定のルールを適用します：
        - ハイフン/マイナス記号を半角'-'に統一
        - 長音記号を全角'ー'に統一
        - チルダを全角'～'に統一
        - 感嘆符を半角'!'に統一
        - 疑問符を半角'?'に統一
        - スペースを半角スペース' 'に統一

        正規化ルールは以下を参考にしています：
        https://github.com/ikegami-yukino/jaconv

        Returns:
            pl.Expr: 正規化された文字列を表す式
        """
        # 1. NFKC正規化を適用
        normalized_expr = self._expr.str.normalize("NFKC")

        # 2. 日本語特有の正規化ルールをreplace_allを使用して適用
        normalized_expr = (
            normalized_expr
            # 長音記号の統一（全角'ー'に）
            .str.replace_all(r"[〜～﹣－—―━─]", "ー", literal=False)
            # ハイフン類の統一（半角'-'に）
            .str.replace_all(r"[―‐˗֊‐‑‒–⁃⁻₋−]", "-", literal=False)
            # クォートの統一
            .str.replace_all("'", "'", literal=True)
            .str.replace_all('"', '"', literal=True)
            .str.replace_all('"', "``", literal=True)
            # 感嘆符を半角に
            .str.replace_all("！", "!", literal=True)
            # 疑問符を半角に
            .str.replace_all("？", "?", literal=True)
            # スペースの統一
            .str.replace_all("　", " ", literal=True)
            .str.replace_all(r"\s+", " ", literal=False)
            .str.strip_chars()
        )
        return normalized_expr
