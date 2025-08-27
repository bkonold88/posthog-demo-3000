# HogFlix Demo 3000

This repository allows you to spin up a demo app which has been instrumented with PostHog, and seed PostHog historic data and artifacts to provide a full-featured demo environment showcasing all features.

## Prerequisites

If you choose to run the demo entirely in your browser using GitHub Code Spaces, skip the requirements and go straight to Option 3, otherwise follow the prerequisites instructions. 

To run the demo app on a Mac you'll need to set up Python 3 locally:

1. Install Xcode Command Line Tools if you haven't already: `xcode-select --install`.
2. Install the package manager Homebrew by following the [instructions here](https://brew.sh/).

After installation, make sure to follow the instructions printed in your terminal to add Homebrew to your `$PATH`. Otherwise, the command line will not know about packages installed with Homebrew.

3. Install Python: `brew install python`.
4. Upgrade pip to the latest version: `pip install -U pip`
5. From the root of this repository, install the requirements: `pip install -r requirements.txt`

## Running the app

There are three ways to run the app: locally using Python, via Docker, or using GitHub Codespaces. 

### Option 1 - Run Locally with Python

Before running the app for the first time, you'll need to create and seed the local SQLite database:

```bash
python pop_db.py
python dummy_data.py
```

This only needs to be done the first time you run the app.

Next, set your PostHog Host and Project API key as environment variables. You can either rename `.env.example` to `.env` and update the placeholder variables therein, or run the following:

```bash
export PH_HOST='https://<eu or us>.i.posthog.com'
export PH_PROJECT_KEY='<Project API key>'
```

Finally, run the app:

```bash
python app.py
```

If you open up a browser and head to `http://127.0.0.1:5000/`, you'll see the HogFlix app running. Use `Ctrl + C` in your terminal to stop the app.

### Option 2 - Run as a Container with Docker

The container hasn't been pushed to a registry yet, so you'll need to build and run it yourself. Make sure you have [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/) installed.

In the root of the repository, first build the container:

```bash
docker build --no-cache --tag posthog-hogflix-demo .
```

Then run the container in detached mode (background):

```bash
docker run -d -p 5000:5000 -e PH_PROJECT_KEY=<Project API key> -e PH_HOST='https://<eu or us>.i.posthog.com' posthog-hogflix-demo
```

You can then access the app on `localhost:5000`.

### Option 3 - Run in GitHub Codespaces

For a seamless setup, you can run the demo entirely in your browser using **GitHub Codespaces**. This avoids needing to manage Python or Docker on your local machine.

To get started:

1. Go to the repository in GitHub.
2. Click on the **Code** button.
3. Navigate to the **Codespaces** tab and click **Create Codespace on Main**.

This will create a virtual environment in your browser where you can run the app and make changes. It may take a few minutes for the environment to configure, but once done, everything will be set up automatically.

You can optionally pass environment variables when creating the Codespace so your `.env` is created automatically:

- `PH_PROJECT_KEY`: Your PostHog Project API key
- `PH_HOST`: Your PostHog host, e.g. `https://us.i.posthog.com` or `https://eu.i.posthog.com`

On creation, the devcontainer will:

- Install dependencies
- Create `.env` from `.env.example` (injecting the provided `PH_*` values if present)
- Initialize the local database and seed dummy stats
- If `PH_*` are provided, also run the historical event seeding script

Run the app:
```bash
make run
```

## Seed Historic Usage Data

To generate valuable insights in your PostHog project, you'll need to add some historic event data. The `seed_demo_data.py` script creates pseudo-random data that mimics real usage of the HogFlix app. You'll need the `500_names_and_emails.csv` in your `scripts` folder (see below on how to generate this), and then run:

```bash
make seed DAYS=30 ITER=100
```

The seeding script will read `PH_PROJECT_KEY` and `PH_HOST` from either your environment or your `.env`. You can still pass `-k` and `-p` flags explicitly if you prefer.

Parameters:
- `-d`: Number of previous days to generate (default 30)
- `-i`: Number of iterations (default 100)

After a few minutes, you'll see newly created events and people in your PostHog project.

## Create Demo Artifacts

Once historic data has been generated, you'll need some PostHog artifacts to view as part of the demo. The `create_posthog_artifacts.py` script adds in:

- Actions looking at pageviews and custom events.
- Cohorts based on behavior and user properties.
- Insights using the above actions.
- A Feature Flag for the action mode feature integrated into the app.

You'll need a **Personal API Key** (available in `/settings/user-api-keys` in the PostHog UI) to run this script:

```bash
PERSONAL_API_KEY=<Personal API Key> POSTHOG_API_BASE_URL="https://<eu or us>.posthog.com/api/projects/<project id>" make artifacts
```

The input parameters are:
- `-k`: Your Personal API key.
- `-p`: The API Endpoint for your PostHog Project.

## Recreate the Seed Data

The `500_names_and_emails.csv` file in the `scripts/` folder contains dummy data for 500 users, which includes group (Family) information. If needed, you can recreate this file by running:

```bash
python scripts/generate_fake_names_and_emails.py
```

## Makefile Shortcuts

Common tasks are wrapped in a `Makefile`:

- `make install`: Install dependencies
- `make env`: Create `.env` from example and inject `PH_*` if set
- `make db`: Initialize and seed local DB
- `make run`: Run the Flask app
- `make seed`: Seed historical events to PostHog (requires `PH_*`)
- `make artifacts`: Create PostHog demo artifacts (requires `PERSONAL_API_KEY` and `POSTHOG_API_BASE_URL`)
- `make test`: Run tests

Then copy the generated file back to the `scripts/` folder to generate more demo data.

---

Now you're ready to demo the full power of PostHog with **HogFlix Demo 3000**!
