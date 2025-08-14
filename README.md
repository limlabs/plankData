# Planck CMB Power Spectrum Models

This application visualizes and compares different cosmological models with Planck CMB power spectrum data:

- Standard ΛCDM Model
- Hilltop Inflation Model
- Starobinsky (R²) Inflation Model

## Features

- Interactive parameter controls for both Hilltop and Starobinsky models
- Real-time visualization updates
- Responsive design that works on all devices
- Single container deployment optimized for AWS App Runner

## Local Development

### Prerequisites

- Python 3.11+
- Node.js 18+
- npm

### Setup

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```

3. Build the frontend:
   ```bash
   npm run build
   ```

4. Run the application:
   ```bash
   python app.py
   ```

The application will be available at http://localhost:8080

## Deployment to AWS App Runner

1. Build the Docker image:
   ```bash
   docker build -t plank-data .
   docker run -p 8080:3000 --name plank-app plank-data 
   ```

2. Tag and push to Amazon ECR:
   ```bash
   aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <account>.dkr.ecr.<region>.amazonaws.com
   docker tag plank-data:latest <account>.dkr.ecr.<region>.amazonaws.com/plank-data:latest
   docker push <account>.dkr.ecr.<region>.amazonaws.com/plank-data:latest
   ```

3. Create an App Runner service using the ECR image
   - Port: 8080
   - CPU: 1 vCPU
   - Memory: 2 GB

## Models

### Hilltop Model Parameters

- `amp`: Overall amplitude scaling (relates to V0)
- `mu`: Mass scale of the potential (typically near Planck scale)
- `v`: Vacuum expectation value (controls oscillation amplitude)
- `p`: Power in potential (p > 2 for inflation)
- `phi`: Initial field value (phi < mu for hilltop inflation)

### Starobinsky Model Parameters

- `amp`: Overall amplitude (sets inflation scale)
- `decay`: Silk damping scale
- `phase`: Acoustic oscillation phase
- `freq`: Sound horizon scale
- `supp`: ISW suppression strength

