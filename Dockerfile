FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Optional system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements*.txt ./
RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi && \
    if [ -f requirements-prod.txt ]; then pip install -r requirements-prod.txt; fi

# Copy code
COPY . .

EXPOSE 8001

# Run Flask through gunicorn (recommended)
CMD ["gunicorn", "-b", "0.0.0.0:8001", "main:app"]
