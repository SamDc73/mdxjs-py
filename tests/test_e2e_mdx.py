"""End-to-end test using a real MDX file."""
from pathlib import Path

import pytest

from mdxjs_py import compile, is_available


@pytest.mark.skipif(not is_available(), reason="Rust module not built")
class TestE2EMDX:
    def test_compile_sample_fixture(self):
        """Compile a real MDX fixture and verify JS output looks sane."""
        mdx_path = Path(__file__).parent / "fixtures" / "sample_e2e.mdx"
        assert mdx_path.exists(), f"Missing fixture: {mdx_path}"

        source = mdx_path.read_text(encoding="utf-8")
        result = compile(source)

        # Basic sanity checks
        assert isinstance(result, str)
        assert len(result) > 0
        assert "function" in result or "export" in result.lower()

    def test_compile_with_options(self):
        """Ensure options flow to Rust layer without errors."""
        mdx_path = Path(__file__).parent / "fixtures" / "sample_e2e.mdx"
        source = mdx_path.read_text(encoding="utf-8")

        # Automatic runtime
        out_auto = compile(source, jsx_runtime="automatic")
        assert isinstance(out_auto, str)

        # Classic runtime
        out_classic = compile(source, jsx_runtime="classic", pragma="h", pragma_frag="Fragment")
        assert isinstance(out_classic, str)
