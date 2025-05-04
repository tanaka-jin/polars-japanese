import polars as pl


class NormalizeExpr:
    """
    Polars Expression for Japanese text normalization.

    This class provides methods to normalize Japanese
    text within Polars expressions,
    based on NFKC normalization followed by specific
    Japanese character replacements.
    """

    def __init__(self, expr: pl.Expr):
        self._expr = expr

    def normalize(self) -> pl.Expr:
        """
        Normalize Japanese text in the expression.

        Applies NFKC normalization first, then applies specific rules:
        - Unifies hyphens/minus signs to half-width '-'.
        - Unifies long vowel sounds to full-width 'ー'.
        - Unifies tildes to full-width '～'.
        - Unifies exclamation marks to half-width '!'.
        - Unifies question marks to half-width '?'.
        - Unifies spaces to a single half-width space ' '.

        Returns:
            pl.Expr: An expression representing the normalized strings.
        """
        # 1. Apply NFKC normalization
        normalized_expr = self._expr.str.normalize("NFKC")

        # 2. Apply Japanese-specific normalization rules using replace_all
        #    Note: Order might matter depending on the rules.
        #    NFKC should handle most full-width/half-width conversions
        #    for standard characters.
        #    We focus on specific symbols mentioned in jaconv's documentation.
        normalized_expr = (
            normalized_expr
            # Unify hyphens/minus signs to half-width '-'
            .str.replace_all(r"[－‐]", "-", literal=False)
            # Ensure long vowel sound is full-width 'ー'
            # (NFKC might handle this, but explicitly ensure)
            # .str.replace_all("ｰ", "ー", literal=True)
            # # NFKC likely covers this
            # Unify tildes to full-width '～'
            .str.replace_all("～", "~", literal=True)
            # Unify exclamation marks to half-width '!'
            # (NFKC likely covers this)
            .str.replace_all("！", "!", literal=True)
            # Unify question marks to half-width '?'
            # (NFKC likely covers this)
            .str.replace_all("？", "?", literal=True)
            # Unify spaces: replace full-width space and
            # collapse multiple spaces
            .str.replace_all(
                "　", " ", literal=True
            )  # Full-width to half-width
            .str.replace_all(
                r"\s+", " ", literal=False
            )  # Collapse multiple spaces
            .str.strip_chars()  # Trim leading/trailing whitespace
        )
        return normalized_expr
