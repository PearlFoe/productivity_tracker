ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH=$PATH:/app/.venv/bin
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY uv.lock .
COPY pyproject.toml .

RUN python -m pip install uv
RUN python -m uv sync --frozen

COPY tasks /app/tasks
COPY secrets /app/secrets
