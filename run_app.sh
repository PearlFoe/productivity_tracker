#!/bin/bash
uv run alembic upgrade head

echo -e "\n\nLoading reference data.\n\n"
uv run prefect deploy --all  # deploy prefect flows
uv run python pt_bot/main.py