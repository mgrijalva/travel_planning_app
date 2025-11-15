FROM python:3.13-slim

# Keep Python output buffered (helpful for logs)
ENV PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

# Install uv package manager and build deps for packages like psycopg2
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev gcc curl \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.local/bin:$PATH"

# Copy only pyproject.toml and README early to leverage Docker cache
COPY pyproject.toml README.md ./

# Install python deps from pyproject.toml using uv
RUN uv pip install --system -r pyproject.toml

# Copy app source
COPY travel_app ./travel_app
COPY migrations ./migrations

EXPOSE 8000

# Run the app with gunicorn using the application factory
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "travel_app.server:create_app()"]
