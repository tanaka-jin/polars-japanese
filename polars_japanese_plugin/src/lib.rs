use pyo3::prelude::*;

mod expressions;

#[pymodule]
#[pyo3(name="polars_japanese_plugin")]
fn _polars_japanese_plugin(_py: Python, _m: &Bound<'_, PyModule>) -> PyResult<()> {
    // ここで expressions モジュール内の関数などを登録する必要があるかもしれません
    // 例: _m.add_function(wrap_pyfunction!(expressions::some_function, _m)?)?;
    Ok(())
}
