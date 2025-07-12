FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-fra \
    poppler-utils \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for better caching
COPY requirements_fixed.txt .
RUN pip install --no-cache-dir -r requirements_fixed.txt

# Copy application
COPY . .

# Create necessary directories
RUN mkdir -p logs data/drop_zone uploads

# Expose port
EXPOSE 5000

# Start command
CMD ["python", "backend/main.py"]
