"""Local PostgreSQL connection smoke test for Sultan Data Platform."""

from __future__ import annotations

import sys

import psycopg2

from config import build_postgres_dsn, load_settings


def main() -> int:
    settings = load_settings()

    try:
        with psycopg2.connect(
            build_postgres_dsn(settings.postgres),
            connect_timeout=5,
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT version(), current_database(), current_user;")
                version, database, user = cursor.fetchone()
    except Exception as exc:
        print("PostgreSQL connection failed.")
        print(f"Error type: {type(exc).__name__}")
        print(f"Error: {exc}")
        return 1

    print("PostgreSQL connection successful.")
    print(f"Database: {database}")
    print(f"User: {user}")
    print(f"Version: {version}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

