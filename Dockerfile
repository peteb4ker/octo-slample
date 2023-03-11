FROM python:3.11.1-slim-bullseye AS octo_slample

WORKDIR /app

RUN apt-get update && \
    apt-get -y --no-install-recommends install gcc=4:10.2.1-1 \
    libasound2-dev=1.2.4-1.1 libc6-dev=2.31-13+deb11u5 libsndfile1-dev=1.0.31-2 && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry==1.3.2

COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY . /app
