"""Configuration helpers for Sultan Data Platform local flows."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


DATA_PLATFORM_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = DATA_PLATFORM_DIR.parent
DEFAULT_ENV_FILE = DATA_PLATFORM_DIR / ".env"


@dataclass(frozen=True)
class PostgresSettings:
    host: str
    port: int
    database: str
    user: str
    password: str
    sslmode: str


@dataclass(frozen=True)
class DataPlatformSettings:
    project_root: Path
    data_platform_dir: Path
    data_dir: Path
    raw_data_dir: Path
    curated_data_dir: Path
    features_data_dir: Path
    pipeline_log_dir: Path
    default_exchange: str
    default_symbols: tuple[str, ...]
    default_timeframes: tuple[str, ...]
    postgres: PostgresSettings


def _split_csv(value: str) -> tuple[str, ...]:
    return tuple(item.strip() for item in value.split(",") if item.strip())


def load_settings(env_file: Path | None = None) -> DataPlatformSettings:
    """Load settings from environment variables and optional local .env."""

    selected_env_file = env_file or DEFAULT_ENV_FILE
    if selected_env_file.exists():
        load_dotenv(selected_env_file)

    project_root = Path(os.getenv("SULTAN_PROJECT_ROOT", str(PROJECT_ROOT))).expanduser()
    data_platform_dir = Path(
        os.getenv("SULTAN_DATA_PLATFORM_DIR", str(DATA_PLATFORM_DIR))
    ).expanduser()
    data_dir = Path(os.getenv("SULTAN_DATA_DIR", str(project_root / "data"))).expanduser()

    return DataPlatformSettings(
        project_root=project_root,
        data_platform_dir=data_platform_dir,
        data_dir=data_dir,
        raw_data_dir=Path(
            os.getenv("SULTAN_RAW_DATA_DIR", str(data_dir / "raw"))
        ).expanduser(),
        curated_data_dir=Path(
            os.getenv("SULTAN_CURATED_DATA_DIR", str(data_dir / "curated"))
        ).expanduser(),
        features_data_dir=Path(
            os.getenv("SULTAN_FEATURES_DATA_DIR", str(data_dir / "features"))
        ).expanduser(),
        pipeline_log_dir=Path(
            os.getenv(
                "SULTAN_PIPELINE_LOG_DIR",
                str(data_platform_dir / "logs" / "pipeline_runs"),
            )
        ).expanduser(),
        default_exchange=os.getenv("SULTAN_DEFAULT_EXCHANGE", "binance"),
        default_symbols=_split_csv(os.getenv("SULTAN_DEFAULT_SYMBOLS", "BTCUSDT,ETHUSDT")),
        default_timeframes=_split_csv(os.getenv("SULTAN_DEFAULT_TIMEFRAMES", "1d,4h")),
        postgres=PostgresSettings(
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=int(os.getenv("POSTGRES_PORT", "5432")),
            database=os.getenv("POSTGRES_DB", "sultan_ai"),
            user=os.getenv("POSTGRES_USER", "sultan_user"),
            password=os.getenv("POSTGRES_PASSWORD", ""),
            sslmode=os.getenv("POSTGRES_SSLMODE", "prefer"),
        ),
    )


def build_postgres_dsn(settings: PostgresSettings) -> str:
    """Build a psycopg2 DSN without exposing it through logs by default."""

    return (
        f"host={settings.host} "
        f"port={settings.port} "
        f"dbname={settings.database} "
        f"user={settings.user} "
        f"password={settings.password} "
        f"sslmode={settings.sslmode}"
    )

