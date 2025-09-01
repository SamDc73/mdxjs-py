//! Python bindings for mdxjs-rs

use mdxjs;
use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;

/// compile(source, options?) - Compile MDX to JavaScript
///
/// Direct binding to mdxjs::compile function
#[pyfunction]
#[pyo3(signature = (source, *, development=None, jsx=None, jsx_import_source=None, jsx_runtime=None, pragma=None, pragma_frag=None, pragma_import_source=None, provider_import_source=None))]
fn compile(
    source: &str,
    development: Option<bool>,
    jsx: Option<bool>,
    jsx_import_source: Option<String>,
    jsx_runtime: Option<String>,
    pragma: Option<String>,
    pragma_frag: Option<String>,
    pragma_import_source: Option<String>,
    provider_import_source: Option<String>,
) -> PyResult<String> {
    // Build options - only set what's provided
    let mut options = mdxjs::Options::default();

    if let Some(dev) = development {
        options.development = dev;
    }

    if let Some(jsx_val) = jsx {
        options.jsx = jsx_val;
    }

    if let Some(source) = jsx_import_source {
        options.jsx_import_source = Some(source);
    }

    if let Some(runtime) = jsx_runtime {
        options.jsx_runtime = match runtime.as_str() {
            "automatic" => Some(mdxjs::JsxRuntime::Automatic),
            "classic" => Some(mdxjs::JsxRuntime::Classic),
            _ => return Err(PyValueError::new_err("jsx_runtime must be 'automatic' or 'classic'"))
        };
    }

    if let Some(p) = pragma {
        options.pragma = Some(p);
    }

    if let Some(pf) = pragma_frag {
        options.pragma_frag = Some(pf);
    }

    if let Some(pi) = pragma_import_source {
        options.pragma_import_source = Some(pi);
    }

    if let Some(pi) = provider_import_source {
        options.provider_import_source = Some(pi);
    }

    // Compile MDX
    match mdxjs::compile(source, &options) {
        Ok(result) => Ok(result),
        Err(err) => Err(PyValueError::new_err(format!("{}", err)))
    }
}

/// compile_sync(source, options?) - Synchronous version of compile
///
/// Alias for compile since Rust version is already sync
#[pyfunction]
#[pyo3(signature = (source, *, development=None, jsx=None, jsx_import_source=None, jsx_runtime=None, pragma=None, pragma_frag=None, pragma_import_source=None, provider_import_source=None))]
fn compile_sync(
    source: &str,
    development: Option<bool>,
    jsx: Option<bool>,
    jsx_import_source: Option<String>,
    jsx_runtime: Option<String>,
    pragma: Option<String>,
    pragma_frag: Option<String>,
    pragma_import_source: Option<String>,
    provider_import_source: Option<String>,
) -> PyResult<String> {
    compile(
        source,
        development,
        jsx,
        jsx_import_source,
        jsx_runtime,
        pragma,
        pragma_frag,
        pragma_import_source,
        provider_import_source,
    )
}

/// Python module definition
#[pymodule]
fn mdxjs_py(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(compile, m)?)?;
    m.add_function(wrap_pyfunction!(compile_sync, m)?)?;
    Ok(())
}
