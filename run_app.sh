#!/bin/bash
uv run alembic upgrade head

uv run prefect deploy --all  # deploy prefect flows
uv run python pt_bot/main.py