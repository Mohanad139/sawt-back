FROM python:3.11-slim AS base

WORKDIR /app

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies required by audio processing libs
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libffi-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml ./
COPY src/ ./src/
RUN pip install --no-cache-dir .

# Drop to non-root user
RUN useradd --create-home agent
USER agent

ENTRYPOINT ["python", "-m", "sawt.agent"]
CMD ["start"]
