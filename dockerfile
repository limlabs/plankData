FROM cgr.dev/chainguard/python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies (including gunicorn, numpy, matplotlib)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port used by Gunicorn / App Runner
EXPOSE 8080

# Run Flask with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "-w", "4", "app:app"]
