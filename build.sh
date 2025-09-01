#!/bin/bash
# Quick build script for mdxjs-py

set -e

echo "🦀 Building mdxjs-py..."

# Check for Rust
if ! command -v cargo &> /dev/null; then
    echo "❌ Rust not found. Install with:"
    echo "  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"
    exit 1
fi

# Check for maturin
if ! command -v maturin &> /dev/null; then
    echo "📦 Installing maturin..."
    pip install maturin || uv pip install maturin
fi

# Build
echo "🔨 Building Rust module..."
maturin develop --release

# Test
echo "🧪 Testing..."
python -c "
from mdxjs_py import compile, is_available
assert is_available(), 'Module not available'
result = compile('# Test')
print('✅ mdxjs-py is working!')
"

echo "✨ Done!"