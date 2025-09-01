"""Test MDX compilation functionality."""

import pytest

from mdxjs_py import compile, compile_sync, is_available


@pytest.mark.skipif(not is_available(), reason="Rust module not built")
class TestCompile:
    """Test compile function."""

    def test_basic_compilation(self):
        """Test basic MDX compilation."""
        mdx = "# Hello World\n\nThis is **MDX**."
        result = compile(mdx)
        assert isinstance(result, str)
        assert len(result) > 0
        # Should contain JS function
        assert "function" in result

    def test_jsx_compilation(self):
        """Test JSX compilation."""
        mdx = "<Button onClick={() => alert('hi')}>Click</Button>"
        result = compile(mdx)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_code_block(self):
        """Test code block compilation."""
        mdx = """
# Code Example

```python
def hello():
    print("Hello, World!")
```
"""
        result = compile(mdx)
        assert isinstance(result, str)
        assert "hello" in result

    def test_development_mode(self):
        """Test development mode compilation."""
        mdx = "# Test"
        result = compile(mdx, development=True)
        assert isinstance(result, str)
        # Development mode includes more debugging info
        assert len(result) > len(compile(mdx, development=False))

    def test_jsx_runtime_automatic(self):
        """Test automatic JSX runtime."""
        mdx = "<div>Test</div>"
        result = compile(mdx, jsx_runtime="automatic")
        assert isinstance(result, str)

    def test_jsx_runtime_classic(self):
        """Test classic JSX runtime."""
        mdx = "<div>Test</div>"
        result = compile(mdx, jsx_runtime="classic")
        assert isinstance(result, str)

    def test_jsx_import_source(self):
        """Test JSX import source option."""
        mdx = "<div>Test</div>"
        result = compile(
            mdx,
            jsx_runtime="automatic",
            jsx_import_source="preact"
        )
        assert isinstance(result, str)

    def test_compile_sync_alias(self):
        """Test that compile_sync is an alias for compile."""
        mdx = "# Test"
        result1 = compile(mdx)
        result2 = compile_sync(mdx)
        assert result1 == result2


@pytest.mark.skipif(not is_available(), reason="Rust module not built")
class TestValidation:
    """Test MDX validation via compilation."""

    def test_valid_mdx(self):
        """Test that valid MDX compiles without error."""
        valid_cases = [
            "# Heading",
            "**bold** and *italic*",
            "[link](https://example.com)",
            "- list\n- items",
            "`inline code`",
            "```\ncode block\n```",
            "<div>JSX element</div>",
            "Text with {1 + 1} expression",
        ]

        for mdx in valid_cases:
            try:
                compile(mdx)
            except ValueError:
                pytest.fail(f"Valid MDX failed: {mdx}")

    def test_unclosed_jsx_tag(self):
        """Test that unclosed JSX tags raise error."""
        mdx = "<Button>Click me"
        with pytest.raises(ValueError) as exc_info:
            compile(mdx)
        assert "Button" in str(exc_info.value)

    def test_mismatched_jsx_tags(self):
        """Test that mismatched JSX tags raise error."""
        mdx = "<Button>Click</Div>"
        with pytest.raises(ValueError) as exc_info:
            compile(mdx)
        error = str(exc_info.value)
        assert "Button" in error or "Div" in error

    def test_invalid_jsx_expression(self):
        """Test that invalid JSX expressions raise error."""
        mdx = "<Button onClick={}>Empty</Button>"
        with pytest.raises(ValueError) as exc_info:
            compile(mdx)
        assert "expression" in str(exc_info.value).lower()

    def test_unclosed_expression(self):
        """Test that unclosed expressions raise error."""
        mdx = "Text with {unclosed expression"
        with pytest.raises(ValueError) as exc_info:
            compile(mdx)
        error = str(exc_info.value).lower()
        assert "expression" in error or "unexpected" in error

    def test_invalid_import(self):
        """Test that invalid imports raise error."""
        mdx = 'import { Component from "module"'
        with pytest.raises(ValueError) as exc_info:
            compile(mdx)
        assert "import" in str(exc_info.value).lower() or "expected" in str(exc_info.value).lower()

    def test_error_includes_location(self):
        """Test that errors include line/column information."""
        mdx = "# Test\n\n<Button>Unclosed"
        with pytest.raises(ValueError) as exc_info:
            compile(mdx)
        error = str(exc_info.value)
        # Should include line number (3) or position info
        assert "3" in error or "line" in error.lower()


@pytest.mark.skipif(not is_available(), reason="Rust module not built")
class TestEdgeCases:
    """Test edge cases and special scenarios."""

    def test_empty_string(self):
        """Test compilation of empty string."""
        result = compile("")
        assert isinstance(result, str)

    def test_only_whitespace(self):
        """Test compilation of whitespace-only content."""
        result = compile("   \n\n   \t")
        assert isinstance(result, str)

    def test_unicode_content(self):
        """Test compilation with Unicode characters."""
        mdx = "# 你好世界 🌍\n\nTesting émojis and ñon-ASCII çharacters."
        result = compile(mdx)
        assert isinstance(result, str)

    def test_large_document(self):
        """Test compilation of large document."""
        mdx = "# Heading\n\nParagraph.\n\n" * 1000
        result = compile(mdx)
        assert isinstance(result, str)
        assert len(result) > 1000

    def test_nested_jsx(self):
        """Test deeply nested JSX elements."""
        mdx = """
<div>
  <section>
    <article>
      <p>Nested content</p>
    </article>
  </section>
</div>
"""
        result = compile(mdx)
        assert isinstance(result, str)

    def test_mixed_content(self):
        """Test MDX with mixed markdown and JSX."""
        mdx = """
# Heading

Regular **markdown** with <Button>JSX</Button> mixed in.

<Alert type="info">
  This is a JSX component with **markdown** inside.
</Alert>

```js
console.log("code block");
```
"""
        result = compile(mdx)
        assert isinstance(result, str)


@pytest.mark.skipif(not is_available(), reason="Rust module not built")
class TestOptions:
    """Test compilation options."""

    def test_jsx_keep_option(self):
        """Test keeping JSX without compilation."""
        mdx = "<Button>Test</Button>"
        result = compile(mdx, jsx=True)
        assert isinstance(result, str)
        # When jsx=True, JSX should be preserved
        # (exact behavior depends on mdxjs-rs)

    def test_pragma_options(self):
        """Test pragma options for classic runtime."""
        mdx = "<div>Test</div>"
        result = compile(
            mdx,
            jsx_runtime="classic",
            pragma="h",
            pragma_frag="Fragment"
        )
        assert isinstance(result, str)

    def test_invalid_jsx_runtime(self):
        """Test that invalid jsx_runtime raises error."""
        mdx = "# Test"
        with pytest.raises(ValueError) as exc_info:
            compile(mdx, jsx_runtime="invalid")
        assert "automatic" in str(exc_info.value) or "classic" in str(exc_info.value)


def test_is_available():
    """Test is_available function."""
    # This test should always pass in CI where module is built
    available = is_available()
    assert isinstance(available, bool)
    # If we got this far in other tests, it should be True
    if available:
        # Try to compile something
        compile("# Test")
    else:
        # Module not built, compilation should fail
        with pytest.raises((ImportError, AttributeError)):
            compile("# Test")
