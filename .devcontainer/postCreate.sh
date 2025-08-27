#!/usr/bin/env bash
set -euo pipefail

# Resolve project root relative to this script (works in Codespaces and local devcontainers)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

python -m pip install -U pip || true
pip install -r requirements.txt || true

# Create .env from example if missing
if [ ! -f .env ]; then
  cp .env.example .env
fi

echo "postCreate complete. Update .env with your PostHog values, then run: make run"

