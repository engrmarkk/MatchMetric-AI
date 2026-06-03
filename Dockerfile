# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django application code
COPY . /app/

EXPOSE 8001

# Run with Gunicorn using Uvicorn workers (ASGI)
CMD ["gunicorn", "resumeai_proj.asgi:application", "--bind", "0.0.0.0:8001", "--worker-class", "uvicorn.workers.UvicornWorker"]