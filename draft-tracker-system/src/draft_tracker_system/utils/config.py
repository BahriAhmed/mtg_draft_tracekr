import yaml
from pathlib import Path


def load_credentials():
    config_path = Path("conf/local/credentials.yml")

    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_db_url():
    creds = load_credentials()["credentials"]["postgres_db"]

    return (
        f"postgresql+psycopg2://{creds['user']}:{creds['password']}"
        f"@{creds['host']}:{creds['port']}/{creds['db']}"
    )