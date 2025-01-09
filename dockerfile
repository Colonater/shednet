# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies (ffmpeg for audio processing)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Create necessary directories
RUN mkdir -p /app/static/music \
    /app/static/boxart \
    /app/static/consoles \
    /app/static/uploads \
    /app/static/library \
    /app/data


# Development or Production
ARG ENVIRONMENT=production
ENV FLASK_ENV=${ENVIRONMENT}

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Environment variables
ENV FLASK_APP=shed.py
ENV FLASK_ENV=production
ENV PORT=5045


# Run the application
CMD ["python", "shed.py"]
