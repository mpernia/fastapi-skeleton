FROM python:3.9-slim

WORKDIR /app

# Add the current directory to PYTHONPATH
ENV PYTHONPATH=/app:$PYTHONPATH

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir wheel && \
    pip install --no-cache-dir -r requirements.txt

# Create static directory
RUN mkdir -p /app/static

# Copy application
COPY . .

# Create non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Run the application
CMD ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
