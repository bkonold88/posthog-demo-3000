### Summary
Streamlined developer setup and seeding for Codespaces with a minimal `.env`, idempotent artifact creation, and a single `make run` workflow.

### What’s changed
- **Devcontainer**
  - Switched image to `mcr.microsoft.com/devcontainers/python:3.12` for faster startup.
  - `.devcontainer/postCreate.sh` resolves project root dynamically and copies `.env.example` to `.env` first.
  - Removed Codespaces env mapping (users now set PH_* in `.env` manually).

- **Environment**
  - Minimal `.env.example` with only:
    - `PH_HOST`
    - `PH_PROJECT_KEY`
    - `PH_PERSONAL_API_KEY`
    - `PH_PROJECT_ID`
  - Post-create sanitizes existing `.env` (resets to example if invalid/duplicated).

- **Makefile**
  - Added `check-env` gate and `env-reset`.
  - Unified `make run`: `check-env` → DB init → seed historical data → create artifacts → run app.
  - `seed` reads PH_* from `.env` (CLI flags still supported).

- **Seeding/Artifacts**
  - `scripts/seed_demo_data.py`: robust CSV path (relative to script), auto-loads `.env`; CLI flags optional.
  - `scripts/create_posthog_artifacts.py`: idempotent (reuses existing actions/cohorts/insights/flags), reads PH_* from `.env`, derives API URL from `PH_HOST`/`PH_PROJECT_ID`.

- **Docs/Tests**
  - `README.md` updated for the new flow (manual `.env` → `make run`).
  - Tests assert `.env.example` contents and script path robustness.
  - `requirements.txt` includes `pytest`.

### How to use
1) Update `.env` with real values:
```bash
PH_HOST='https://<eu or us>.i.posthog.com'
PH_PROJECT_KEY='<Project API key>'
PH_PERSONAL_API_KEY='<Personal API key>'
PH_PROJECT_ID='<Project Id>'
```

2) Run:
```bash
make run
```
This verifies `.env`, initializes the local DB, seeds historical data into PostHog, creates demo artifacts, and starts the app.

### Notes
- Artifact creation is idempotent and safe even if multiple Codespaces share the same PostHog project.
- If `.env` gets messy, reset it:
```bash
make env-reset
```
