use pyo3::prelude::*;

mod expressions;

#[pymodule]
#[pyo3(name="polars_japanese_plugin")]
fn _polars_japanese_plugin(_py: Python, _m: &Bound<'_, PyModule>) -> PyResult<()> {
    Ok(())
}
