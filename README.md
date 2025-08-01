# DigitalOcean AI Automation

A FastAPI application containerized with Docker.
AI Automation for source code generation to deploy on DigitalOcean Droplets/VPS-Virtual Private Server using DigitalOcean Container Registry

## Prerequisites

- Python 3.13+
- Docker
- Docker Compose (optional)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/accelcq/DigitalOceanAIAutomation.git
cd DigitalOceanAIAutomation
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### Local Development
```bash
uvicorn main:app --reload
```

### Docker
```bash
docker build -t digitaloceanaiautomation .
docker run -p 8000:8000 digitaloceanaiautomation
```

## API Documentation

Once the application is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Dependencies

- FastAPI 0.115.0
- Uvicorn 0.30.6

## Version Control & GitHub Deployment

### Initial Setup
```bash
# Initialize git repository
git init

# Add GitHub remote using accelcq account
git remote add origin https://github.com/accelcq/DigitalOceanAIAutomation.git

# Configure git user (if not already configured)
git config user.name "accelcq"
git config user.email "your-email@example.com"
```

### Pushing Code to GitHub
```bash
# Add all files to staging
git add .

# Commit changes
git commit -m "Initial commit: digitaloceanaiautomation project setup"

# Push to main branch
git push -u origin main
```

### Subsequent Updates
```bash
# Add changes
git add .

# Commit with descriptive message
git commit -m "Your commit message here"

# Push to GitHub
git push origin main
```

## License

This project is licensed under the MIT License.