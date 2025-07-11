# Service OCR avec GPU
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

WORKDIR /app

# Install system dependencies for OCR
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    easyocr \
    opencv-python \
    Pillow \
    PyPDF2 \
    flask

# Download EasyOCR models during build
RUN python -c "import easyocr; reader = easyocr.Reader(['en', 'fr'])"

# Copy OCR service files
COPY backend/services/ocr_service.py ./

# Expose port
EXPOSE 5003

# Run OCR service
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5003"]
