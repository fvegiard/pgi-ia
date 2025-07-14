# PGI-IA Backend Dockerfile
# Production-ready Flask backend with DeepSeek integration

FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./backend/
COPY scripts/ ./scripts/
COPY datasets/ ./datasets/
COPY config/ ./config/
COPY models/ ./models/
COPY data/ ./data/

# Create necessary directories
RUN mkdir -p logs uploads

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=backend/main.py
ENV FLASK_ENV=production

# Expose port
EXPOSE 5000

# Run Flask application
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]