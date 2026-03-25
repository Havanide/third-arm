#!/usr/bin/env bash
# ── Third Arm — dev server launcher ─────────────────────────────────────────────
# Usage: bash scripts/dev.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

# Activate venv if present
if [[ -f ".venv/bin/activate" ]]; then
  source .venv/bin/activate
fi

# Copy .env.example → .env if not present
if [[ ! -f ".env" ]]; then
  echo "⚠  .env not found — copying from .env.example"
  cp .env.example .env
fi

echo "🦾 Starting Third Arm dev server..."
uvicorn third_arm.main:app \
  --reload \
  --host 0.0.0.0 \
  --port 8080 \
  --log-level debug
