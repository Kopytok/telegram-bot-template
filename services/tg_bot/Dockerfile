FROM python:3.12-slim

WORKDIR /app

# Build deps for aiohttp
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libc-dev libffi-dev \
 && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install --no-cache-dir uv

# Install dependencies into a managed .venv
COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev

# Copy source code
COPY src ./src

# Use uv-created venv Python
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:${PATH}"
ENV PYTHONPATH=/app/src

CMD ["python", "-m", "bot.main"]
