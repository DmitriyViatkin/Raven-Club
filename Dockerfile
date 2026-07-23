FROM python:3.12-slim
LABEL authors="dima"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl gettext \
    && rm -rf /var/lib/apt/lists/*

# Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry
RUN poetry config virtualenvs.create false
RUN poetry self add poetry-plugin-export

# Копируем зависимости отдельно от кода - для кэша слоёв
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --without-hashes -o requirements.txt && \
    pip install --no-cache-dir -r requirements.txt && \
    rm requirements.txt

COPY . .

RUN chmod +x /app/docker-entrypoint.sh

RUN adduser --disabled-password --gecos '' appuser && \
    mkdir -p /app/staticfiles /app/media && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

ENTRYPOINT ["/app/docker-entrypoint.sh"]