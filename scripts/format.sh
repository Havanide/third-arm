#!/usr/bin/env bash
# ── Third Arm — format and lint ──────────────────────────────────────────────────
# Usage: bash scripts/format.sh
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

echo "🎨 Formatting with ruff..."
ruff format src/ tests/ scripts/

echo "🔍 Linting with ruff..."
ruff check src/ tests/ scripts/ --fix

echo "✅ Done"
