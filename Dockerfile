# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    API_PORT=8000

# Create a non-root user
RUN adduser --disabled-password --gecos '' appuser
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application code
COPY . .

# Change to non-root user
USER appuser

# Expose FastAPI port (use API_PORT env variable)
EXPOSE $API_PORT

# Default command: run FastAPI app with uvicorn on API_PORT
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $API_PORT"] 