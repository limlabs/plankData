FROM python:3.11-slim

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

# Run with Gunicorn in production mode
# -w 4: 4 worker processes
# -b 0.0.0.0:8080: bind to all interfaces on port 8080
# --access-logfile -: log to stdout
# app:app: use app.py and look for 'app' variable
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "--access-logfile", "-", "app:app"]
