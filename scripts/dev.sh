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

readarray -t UVICORN_ARGS < <(python - <<'PY'
from third_arm.core.settings import get_settings

cfg = get_settings()

print(cfg.host)
print(cfg.port)
print(str(cfg.log_level).lower())
print("true" if cfg.reload else "false")
PY
)

HOST="${UVICORN_ARGS[0]}"
PORT="${UVICORN_ARGS[1]}"
LOG_LEVEL="${UVICORN_ARGS[2]}"
RELOAD="${UVICORN_ARGS[3]}"

UVICORN_CMD=(uvicorn third_arm.main:app --host "$HOST" --port "$PORT" --log-level "$LOG_LEVEL")
if [[ "$RELOAD" == "true" ]]; then
  UVICORN_CMD+=(--reload)
fi

"${UVICORN_CMD[@]}"
