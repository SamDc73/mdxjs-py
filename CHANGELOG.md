# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0-alpha.1] - 2024-12-XX

### Added
- Initial alpha release
- `compile()` function for MDX to JavaScript compilation
- `compile_sync()` alias for API compatibility
- `is_available()` function to check module availability
- Support for all mdxjs-rs compile options:
  - `development` mode
  - `jsx` preservation
  - `jsx_runtime` (automatic/classic)
  - `jsx_import_source`
  - `pragma` and `pragma_frag`
  - `pragma_import_source`
  - `provider_import_source`
- Comprehensive error messages with line/column information
- Type hints and py.typed marker
- Linux x86_64 wheel support

### Notes
- This is an alpha release - API may change
- Only Linux x86_64 wheels provided initially
- Other platforms require Rust toolchain for building

[Unreleased]: https://github.com/SamDc73/mdxjs-py/compare/v0.1.0-alpha.1...HEAD
[0.1.0-alpha.1]: https://github.com/SamDc73/mdxjs-py/releases/tag/v0.1.0-alpha.1
