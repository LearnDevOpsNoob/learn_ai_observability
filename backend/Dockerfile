# ------------------------
# Builder Stage
# ------------------------
# FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

# WORKDIR /app

# # Enable bytecode compilation
# ENV UV_COMPILE_BYTECODE=1
# ENV UV_LINK_MODE=copy

# COPY pyproject.toml uv.lock ./

# RUN uv sync --frozen --no-dev

# COPY . .

# RUN uv sync --frozen --no-dev

# Understand more about tis build stage it might teach much more about uv, and linux as well

# ------------------------
# Runtime Stage
# ------------------------

# FROM python:3.13-slim

# WORKDIR /app

# COPY --from=builder /app /app

# ENV PATH="/app/.venv/bin:$PATH"

# EXPOSE 8000

# CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]


FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

COPY . .

RUN uv sync --frozen --no-dev

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
