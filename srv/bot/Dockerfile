FROM python:3.12-slim

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONPATH=/app \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # Poetry's configuration:
  POETRY_NO_INTERACTION=true \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local'

RUN pip install poetry
WORKDIR /app
COPY README.md pyproject.toml poetry.lock ./
RUN --mount=type=cache,target=/root/.cache \
    poetry install --no-root

COPY .env ./.env
COPY ./src ./src

WORKDIR /app/src/bot

CMD ["python", "main.py"]