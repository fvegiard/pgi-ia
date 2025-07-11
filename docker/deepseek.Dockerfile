# Service DeepSeek avec support GPU
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir \
    transformers \
    datasets \
    peft \
    bitsandbytes \
    accelerate \
    deepspeed \
    flask \
    requests

# Copy DeepSeek specific files
COPY deepseek_*.py ./
COPY train_deepseek_*.py ./

# Create directories
RUN mkdir -p models deepseek_training_complete

# Expose port for API
EXPOSE 5002

# Run service
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5002"]
