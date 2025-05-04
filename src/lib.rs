use pyo3::prelude::*;

mod expressions;

#[pymodule]
#[pyo3(name="polars_japanese")]
fn _polars_japanese(_py: Python, _m: &Bound<'_, PyModule>) -> PyResult<()> {
    Ok(())
}
