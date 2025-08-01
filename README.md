# FastAPI Docker Project

A FastAPI application containerized with Docker.

## Prerequisites

- Python 3.8+
- Docker
- Docker Compose (optional)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/accelcq/fastapi-docker.git
cd fastapi-docker
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
docker build -t fastapi-docker .
docker run -p 8000:8000 fastapi-docker
```

## API Documentation

Once the application is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Dependencies

- FastAPI 0.115.0
- Uvicorn 0.30.6

## License

This project is licensed under the MIT License.