# Multi-stage lightweight Dockerfile for Python Calculator App
FROM python:3.12-slim AS base

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY app/ ./app/

# Create a non-root user for security best practices
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Expose port (if web enabled) or define container entrypoint
ENV PYTHONUNBUFFERED=1
CMD ["python", "app/calculator.py"]
