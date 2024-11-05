#!/bin/bash
uv run alembic upgrade head

echo -e "\n\nLoading reference data.\n\n"
uv run python3 data/load.py  --file data/sql/reference_data.sql

uv run python src/main.py