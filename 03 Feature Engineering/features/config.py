"""Minimal configuration for 03 Feature Engineering.

The defaults are intentionally local and read-only friendly. Passwords are not
hardcoded; if a local .env exists it may provide POSTGRES_PASSWORD.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


FEATURE_ENGINEERING_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = FEATURE_ENGINEERING_DIR.parent
DATA_FEATURES_DIR = PROJECT_ROOT / "data" / "features"
LOCAL_ENV_FILE = FEATURE_ENGINEERING_DIR / ".env"
DATA_PLATFORM_ENV_FILE = PROJECT_ROOT / "02 Data Platform" / ".env"

DB_NAME = "sultan_ai"
DB_USER = "sultan_user"
DB_HOST = "localhost"
DB_PORT = 5432
OHLCV_TABLE = "public.ohlcv_curated"
FEATURE_SET = "technical_v1"
FEATURE_VERSION = "1.0.0"
DEFAULT_SYMBOLS = ["BTCUSDT", "ETHUSDT"]
DEFAULT_TIMEFRAMES = ["1d", "4h"]
TIMEZONE = "America/Costa_Rica"
DEFAULT_EXCHANGE = "binance"


@dataclass(frozen=True)
class PostgresSettings:
    host: str = DB_HOST
    port: int = DB_PORT
    database: str = DB_NAME
    user: str = DB_USER
    password: str = ""
    sslmode: str = "prefer"


@dataclass(frozen=True)
class FeatureSettings:
    project_root: Path
    feature_engineering_dir: Path
    ohlcv_table: str
    feature_set: str
    feature_version: str
    default_exchange: str
    default_symbols: tuple[str, ...]
    default_timeframes: tuple[str, ...]
    timezone: str
    postgres: PostgresSettings


def _load_optional_env() -> None:
    if load_dotenv is None:
        return
    if LOCAL_ENV_FILE.exists():
        load_dotenv(LOCAL_ENV_FILE)
    elif DATA_PLATFORM_ENV_FILE.exists():
        load_dotenv(DATA_PLATFORM_ENV_FILE)


def _split_csv(value: str) -> tuple[str, ...]:
    return tuple(item.strip() for item in value.split(",") if item.strip())


def load_feature_settings() -> FeatureSettings:
    """Load minimal feature settings from defaults plus optional environment."""

    _load_optional_env()

    return FeatureSettings(
        project_root=Path(os.getenv("SULTAN_PROJECT_ROOT", str(PROJECT_ROOT))).expanduser(),
        feature_engineering_dir=Path(
            os.getenv("SULTAN_FEATURE_ENGINEERING_DIR", str(FEATURE_ENGINEERING_DIR))
        ).expanduser(),
        ohlcv_table=os.getenv("SULTAN_OHLCV_TABLE", OHLCV_TABLE),
        feature_set=os.getenv("SULTAN_FEATURE_SET", FEATURE_SET),
        feature_version=os.getenv("SULTAN_FEATURE_VERSION", FEATURE_VERSION),
        default_exchange=os.getenv("SULTAN_DEFAULT_EXCHANGE", DEFAULT_EXCHANGE),
        default_symbols=_split_csv(
            os.getenv("SULTAN_DEFAULT_SYMBOLS", ",".join(DEFAULT_SYMBOLS))
        ),
        default_timeframes=_split_csv(
            os.getenv("SULTAN_DEFAULT_TIMEFRAMES", ",".join(DEFAULT_TIMEFRAMES))
        ),
        timezone=os.getenv("SULTAN_TIMEZONE", TIMEZONE),
        postgres=PostgresSettings(
            host=os.getenv("POSTGRES_HOST", DB_HOST),
            port=int(os.getenv("POSTGRES_PORT", str(DB_PORT))),
            database=os.getenv("POSTGRES_DB", DB_NAME),
            user=os.getenv("POSTGRES_USER", DB_USER),
            password=os.getenv("POSTGRES_PASSWORD", ""),
            sslmode=os.getenv("POSTGRES_SSLMODE", "prefer"),
        ),
    )


def build_postgres_dsn(settings: PostgresSettings) -> str:
    """Build a psycopg2 DSN without printing secrets."""

    return (
        f"host={settings.host} "
        f"port={settings.port} "
        f"dbname={settings.database} "
        f"user={settings.user} "
        f"password={settings.password} "
        f"sslmode={settings.sslmode}"
    )
