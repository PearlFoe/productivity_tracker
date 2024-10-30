#!/bin/bash
uv run alembic upgrade head  # run migrations
uv run python src/main.py