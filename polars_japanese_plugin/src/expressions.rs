use polars::prelude::*;
use pyo3_polars::derive::polars_expr;
use mojimoji_rs::{zen_to_han, han_to_zen};

/// 全角→半角変換
#[polars_expr(output_type=String)]
pub fn to_half_width(inputs: &[Series]) -> PolarsResult<Series> {
    let ca = inputs[0].str()?;
    let out: StringChunked =
        ca.apply_into_string_amortized(|val, buf| {
            let half_width = zen_to_han(val.to_string(), true, true, true);
            buf.push_str(&half_width)
        });
    Ok(out.into_series())
}

/// 半角→全角変換
#[polars_expr(output_type=String)]
fn to_full_width(inputs: &[Series]) -> PolarsResult<Series> {
    let ca = inputs[0].str()?;
    let out: StringChunked =
        ca.apply_into_string_amortized(|val, buf| {
            let full_width = han_to_zen(val.to_string(), true, true, true);
            buf.push_str(&full_width)
        });
    Ok(out.into_series())
}
