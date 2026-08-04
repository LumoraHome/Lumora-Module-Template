#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

SRC_DIR="$PROJECT_ROOT/src"
BUILD_DIR="$PROJECT_ROOT/build/output"
PACKAGE_DIR="$BUILD_DIR/package"
DIST_DIR="$BUILD_DIR/dist"

cd "$PROJECT_ROOT"

# Ensure Python exists

if ! command -v python3 >/dev/null 2>&1; then
    echo "python3 is required."
    exit 1
fi

# Create venv if missing

if [ ! -d "$SRC_DIR/venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$SRC_DIR/venv"
fi

# Activate

source "$SRC_DIR/venv/bin/activate"

# Upgrade tooling

python -m pip install --upgrade pip setuptools wheel

# Install dependencies

if [ -f "$PROJECT_ROOT/requirements.txt" ]; then
    echo "Installing dependencies..."
    python -m pip install -r "$PROJECT_ROOT/requirements.txt"
fi

# Clean

rm -rf "$BUILD_DIR"

mkdir -p "$PACKAGE_DIR/runtime"
mkdir -p "$PACKAGE_DIR/ui"

# Build

pyinstaller \
    --clean \
    --onefile \
    --windowed \
    --name plugin \
    --distpath "$DIST_DIR" \
    --workpath "$BUILD_DIR/build" \
    --specpath "$BUILD_DIR" \
    "$SRC_DIR/main.py"

# Package

cp "$DIST_DIR/plugin" "$PACKAGE_DIR/runtime/"
cp "$PROJECT_ROOT/manifest.json" "$PACKAGE_DIR/"
cp -r "$PROJECT_ROOT/ui" "$PACKAGE_DIR/"

mkdir -p "$PROJECT_ROOT/output"

(
    cd "$BUILD_DIR"
    zip -r "$PROJECT_ROOT/output/module.zip" "package"
)

echo ""
echo "Package created:"
echo "  output/module.zip"