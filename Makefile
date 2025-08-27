SHELL := /usr/bin/bash

.PHONY: help install env db run seed artifacts test lint clean

help:
	@echo "Common targets:"
	@echo "  make install    - Install Python dependencies"
	@echo "  make env        - Create .env from example (and inject PH_* if set)"
	@echo "  make db         - Initialize DB and dummy stats"
	@echo "  make run        - Run Flask app"
	@echo "  make seed       - Seed PostHog historical data (uses PH_* env)"
	@echo "  make artifacts  - Create PostHog demo artifacts (requires PERSONAL_API_KEY and API base URL)"
	@echo "  make test       - Run tests"

install:
	python -m pip install -U pip
	pip install -r requirements.txt

env:
	@if [ ! -f .env ]; then cp .env.example .env; fi
	@if [ -n "$$PH_PROJECT_KEY" ]; then sed -i "s/^PH_PROJECT_KEY=.*/PH_PROJECT_KEY=$$PH_PROJECT_KEY/" .env; fi
	@if [ -n "$$PH_HOST" ]; then sed -i "s#^PH_HOST=.*#PH_HOST=$$PH_HOST#" .env; fi

db:
	python pop_db.py
	python dummy_data.py

run:
	python app.py

seed:
	python scripts/seed_demo_data.py -d $${DAYS:-30} -i $${ITER:-100}

artifacts:
	@if [ -z "$$PERSONAL_API_KEY" ] || [ -z "$$POSTHOG_API_BASE_URL" ]; then \
		echo "Set PERSONAL_API_KEY and POSTHOG_API_BASE_URL env vars."; exit 1; \
	fi
	python scripts/create_posthog_artifacts.py -k "$$PERSONAL_API_KEY" -p "$$POSTHOG_API_BASE_URL"

test:
	pytest -q

clean:
	rm -f hogflix.sqlite
	rm -f .env
