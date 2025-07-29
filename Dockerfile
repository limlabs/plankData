# Build stage for React frontend
FROM public.ecr.aws/docker/library/node:18-alpine AS frontend-builder
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Main Python stage
FROM public.ecr.aws/docker/library/python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies (including gunicorn, numpy, matplotlib)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Copy the built React app from frontend-builder
COPY --from=frontend-builder /frontend/dist frontend/dist

# Set proper file permissions for security
RUN chown -R nobody:nogroup /app
USER nobody

# Expose the port used by Gunicorn / App Runner
EXPOSE 8080

# Verify build
RUN python -c "import app; print('App module loaded successfully')"

# Run with Gunicorn in production mode
# -w 4: 4 worker processes
# -b 0.0.0.0:8080: bind to all interfaces on port 8080
# --access-logfile -: log to stdout
# app:app: use app.py and look for 'app' variable
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "--access-logfile", "-", "app:app"]
