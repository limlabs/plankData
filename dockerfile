# Use slim Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies for matplotlib and NumPy
RUN apt-get update && apt-get install -y \
    build-essential \
    libfreetype6-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies (including gunicorn)
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# App Runner expects port 8080
EXPOSE 8080

# Run Flask app with Gunicorn on port 8080
CMD ["gunicorn", "-b", "0.0.0.0:8080", "-w", "4", "app:app"]
