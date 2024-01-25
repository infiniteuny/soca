FROM python:3.11-bookworm as builder

WORKDIR /tmp

ENV POETRY_VIRTUALENVS_CREATE=true \
    POETRY_VIRTUALENVS_IN_PROJECT=true

COPY pyproject.toml poetry.lock ./

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=cache,target=/root/.cache/pypoetry \
    pip3 install --upgrade pip && \
    pip3 install poetry && \
    poetry install --no-ansi --no-interaction --no-root

FROM python:3.11-slim-bookworm as runtime

WORKDIR /app

RUN apt-get update && \
    # Required for runtime
    apt-get install -y --no-install-recommends ffmpeg && \
    apt-get clean && \
    rm -rf /tmp/* /var/lib/apt/lists/* /var/tmp/

COPY --from=builder /tmp/.venv /app/.venv
COPY ./soca /app/soca

ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["python3", "-m", "soca.main"]
