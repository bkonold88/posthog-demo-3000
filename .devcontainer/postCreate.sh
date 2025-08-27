#!/usr/bin/env bash
set -euo pipefail

cd /workspace

python -m pip install -U pip || true
pip install -r requirements.txt || true

# Create .env from example if missing
if [ ! -f .env ]; then
  cp .env.example .env
fi

echo "postCreate complete. Update .env with your PostHog values, then run: make run"

