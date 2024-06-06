FROM python:3.12 AS base

ARG BUILD_TYPE=dev

ENV BUILD_TYPE=${BUILD_TYPE} \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.7.0

RUN groupadd -r app \
    && useradd --no-log-init -M -r -g app app
RUN mkdir -p /app/app
RUN chown -R app:app /app

WORKDIR /app

FROM base AS build

# For build stage

RUN echo "Building"
COPY --chown=app:app pyproject.toml /app/
COPY --chown=app:app poetry.lock /app/

# Create virtual environment and install dependencies
RUN python -m venv /venv

# Print the Python version and installed packages
RUN echo "Python Version:" && python --version && \
    echo "Installed packages:" && /venv/bin/pip list

RUN . /venv/bin/activate && \
    chown -R app:app /venv && \
    python -m pip install "poetry==$POETRY_VERSION" && \
    poetry config virtualenvs.create false &&  \
    poetry install --no-interaction --no-ansi \
    $(test "$BUILD_TYPE" = production && echo "--no-dev")

FROM base AS main

USER app:app

COPY --from=build /venv /venv
COPY --from=build /app /app

WORKDIR /app

# Python code

COPY --chown=app:app main.py /app/
RUN mkdir -p /app/app
COPY --chown=app:app app /app/app/

# Docker entrypoint

COPY --chown=app:app docker/docker-entrypoint.sh /app/
RUN chmod u+x docker-entrypoint.sh

# Just env file

ADD --chown=app:app .env /app

EXPOSE 8888

ENTRYPOINT ["/app/docker-entrypoint.sh"]
# CMD ["gunicorn", "main:app", "--workers", "4", "--bind", "0.0.0.0:8888", "--forwarded-allow-ips='*'", "--worker-class", "uvicorn.workers.UvicornWorker"]
# CMD ["uvicorn", "main:app", "--workers", "4", "--host", "0.0.0.0", "--port", "8888" "--forwarded-allow-ips='*'"]

# FROM main AS alembic

# COPY --from=main /venv /venv

# COPY --from=main /app /app

# COPY --chown=app:app alembic.ini /app/

# COPY --chown=app:app alembic/\* /app/alembic/

# CMD ["alembic", "upgrade", "head"]
