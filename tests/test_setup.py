import os
import sys
from pathlib import Path


def test_env_example_exists():
    assert (Path(__file__).resolve().parents[1] / '.env.example').exists()


def test_seed_csv_path_resolves():
    # ensure scripts can access CSV relative to their dir
    csv_path = Path(__file__).resolve().parents[1] / 'scripts' / '500_names_and_emails.csv'
    assert csv_path.exists()


def test_config_env_defaults(monkeypatch):
    monkeypatch.delenv('PH_PROJECT_KEY', raising=False)
    monkeypatch.setenv('PH_HOST', 'https://us.i.posthog.com')
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    from config import Config
    assert Config.PH_HOST.startswith('https://')


def test_env_example_contains_required_keys():
    env_path = Path(__file__).resolve().parents[1] / '.env.example'
    content = env_path.read_text().strip().splitlines()
    expected = {
        "PH_HOST='https://<eu or us>.i.posthog.com'",
        "PH_PROJECT_KEY='<Project API key>'",
        "PH_PERSONAL_API_KEY='<Personal API key>'",
        "PH_PROJECT_ID='<Project Id>'",
        "OPENAI_API_KEY='<OpenAI API key>'",
    }
    assert set(content) == expected
