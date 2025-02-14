FROM python:3.13-slim AS base
WORKDIR /app
RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-cache --without dev
COPY . .

FROM base as docs-0
CMD poetry run python docs.py

FROM node:23-slim as docs
WORKDIR /app
RUN npm i -g @redocly/cli@latest
CMD npx @redocly/cli@latest build-docs openapi.json

FROM base as api
CMD poetry run alembic upgrade head && \
    poetry run uvicorn api.main:app --host 0.0.0.0 --port 8000

FROM base as worker
CMD poetry run celery -A worker.cleanup_refresh_tokens worker -B -c 1 --loglevel=INFO
