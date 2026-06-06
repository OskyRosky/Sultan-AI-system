#!/bin/bash
set -euo pipefail

REPO_DIR="/Users/sultan/Trading/Sultan-AI-system"
LOG_DIR="$REPO_DIR/02 Data Platform/logs/ohlcv_reconciliation"
POETRY_BIN="/Users/sultan/.local/bin/poetry"
RUN_TS="$(date -u '+%Y%m%dT%H%M%SZ')"
RUN_LOG="$LOG_DIR/run_${RUN_TS}.log"

mkdir -p "$LOG_DIR"

exec > >(tee -a "$RUN_LOG") 2> >(tee -a "$RUN_LOG" >&2)

echo "[$(date -u '+%Y-%m-%dT%H:%M:%SZ')] Starting OHLCV reconciliation run"
echo "[$(date -u '+%Y-%m-%dT%H:%M:%SZ')] repo=$REPO_DIR"
echo "[$(date -u '+%Y-%m-%dT%H:%M:%SZ')] mode=incremental"

cd "$REPO_DIR"

export PREFECT_API_URL=
export SULTAN_OHLCV_MODE=incremental

"$POETRY_BIN" run python "02 Data Platform/flows/ingest_ohlcv_flow.py"

echo "[$(date -u '+%Y-%m-%dT%H:%M:%SZ')] Finished OHLCV reconciliation run"
