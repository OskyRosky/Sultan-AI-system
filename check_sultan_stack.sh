#!/bin/bash

echo "======================================"
echo " SULTAN — STACK CHECK"
echo "======================================"
echo ""

echo "## Base tools"
echo "Homebrew: $(brew --version | head -n 1)"
echo "Git: $(git --version)"
echo "VS Code CLI:"
code --version | head -n 3
echo ""

echo "## Python / pyenv"
echo "pyenv: $(pyenv --version)"
echo "Project Python:"
python --version
echo ".python-version:"
cat .python-version
echo "which python:"
which python
echo ""

echo "## Poetry"
echo "Poetry:"
poetry --version
echo "Poetry env:"
poetry env info
echo ""

echo "## PostgreSQL"
psql --version
brew services list | grep postgresql || true
pg_isready -h localhost -p 5432 || true
echo ""

echo "## Redis"
redis-server --version
brew services list | grep redis || true
echo ""

echo "## TA-Lib"
brew list ta-lib >/dev/null 2>&1 && echo "TA-Lib system: installed" || echo "TA-Lib system: not found"
echo ""

echo "## DBeaver"
brew list --cask dbeaver-community >/dev/null 2>&1 && echo "DBeaver: installed" || echo "DBeaver: not found"
echo ""

echo "## Poetry dependencies"
poetry show --top-level
echo ""

echo "## Import test"
poetry run python -c "import pandas, ccxt, duckdb, pyarrow, httpx, prefect, pandera, pydantic, talib, telegram, psycopg2, loguru; print('All Sultan Data Platform imports OK')"
echo ""

echo "======================================"
echo " CHECK COMPLETED"
echo "======================================"

