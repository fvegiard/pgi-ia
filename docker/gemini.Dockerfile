# Service Gemini pour PGI-IA
FROM python:3.12-slim

WORKDIR /app

# Install minimal dependencies
RUN pip install --no-cache-dir \
    google-generativeai \
    PyPDF2 \
    requests \
    flask

# Copy Gemini specific files
COPY gemini_manager.py .
COPY gemini_pgi_integration.py .

# Create directories
RUN mkdir -p plans_kahnawake plans_alexis_nihon results

# API endpoint for Gemini service
EXPOSE 5001

# Run as a service
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5001"]
