#!/bin/bash

# Build script for Tally Integration Library
# This script builds and validates the package for PyPI distribution

echo "🚀 Building Tally Integration Library for PyPI"
echo "================================================"

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/
rm -rf dist/
rm -rf *.egg-info/

# Install build dependencies
echo "📦 Installing build dependencies..."
pip install --upgrade build twine wheel setuptools

# Build the package
echo "🔨 Building the package..."
python -m build

# Check the package
echo "🔍 Checking the package..."
python -m twine check dist/*

# List the built files
echo "📁 Built files:"
ls -la dist/

echo ""
echo "✅ Package built successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Test the package: pip install dist/tally_integration-1.0.0-py3-none-any.whl"
echo "2. Upload to TestPyPI: twine upload --repository testpypi dist/*"
echo "3. Upload to PyPI: twine upload dist/*"
echo ""
echo "📚 Required PyPI account setup:"
echo "- Create account at https://pypi.org/"
echo "- Generate API token"
echo "- Configure ~/.pypirc with credentials"
