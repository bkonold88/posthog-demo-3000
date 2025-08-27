#!/usr/bin/env bash
set -euo pipefail

cd /workspace

python -m pip install -U pip
pip install -r requirements.txt

# Create .env from example if missing
if [ ! -f .env ]; then
  cp .env.example .env
  # If Codespaces env vars are provided, inject them
  if [ -n "${PH_PROJECT_KEY:-}" ]; then
    sed -i "s/^PH_PROJECT_KEY=.*/PH_PROJECT_KEY=${PH_PROJECT_KEY}/" .env || true
  fi
  if [ -n "${PH_HOST:-}" ]; then
    sed -i "s#^PH_HOST=.*#PH_HOST=${PH_HOST}#" .env || true
  fi
fi

# Initialize local DB and dummy stats
python pop_db.py
python dummy_data.py

# Seed PostHog historical data if env is present
if [ -n "${PH_PROJECT_KEY:-}" ] && [ -n "${PH_HOST:-}" ]; then
  echo "Seeding PostHog historical data..."
  python scripts/seed_demo_data.py -d 30 -i 100 || true
fi

echo "postCreate complete."

