#!/bin/bash
uv run alembic upgrade head

echo -e "\n\nLoading reference data.\n\n"
uv run python3 data/load.py  --file data/sql/reference_data.sql
uv run prefect deploy --all  # deploy prefect flows
uv run python pt_bot/main.py