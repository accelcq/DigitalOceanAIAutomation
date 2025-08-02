import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
async def root():
    # Detect environment based on container name or default to dev for dev branch
    environment = "development"
    return {
        "message": f"Hello from DigitalOcean AI Automation - {environment.upper()} Environment!",
        "environment": environment,
        "version": "1.0-dev",
        "deployment": "Deployed using GitHub Actions and Docker automatically on each push to the main branch.",
        "available_endpoints": {
            "GET /": "Root endpoint - shows this API overview",
            "GET /health": "Health check endpoint - returns application status",
            "GET /version": "Version endpoint - returns application version",
            "GET /info": "Info endpoint - returns application information",
            "GET /docs": "Documentation endpoint - Swagger UI documentation",
            "GET /redoc": "Alternative documentation - ReDoc UI",
            "GET /request-info": "Request info endpoint - returns client request details in headers"
        },
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc",
            "openapi_json": "/openapi.json"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "environment": "development"}

@app.get("/version")
async def version():
    return {"version": "1.0.0"}
@app.get("/info")
async def info():
    return {"info": "This is a FastAPI application running on DigitalOcean Droplet."}

@app.get("/docs")
async def get_docs():
    return {"message": "This endpoint provides documentation for the API."}

@app.get("/request-info")
async def get_request_info(request: Request):
    # Extract request information
    request_info = {
        "method": request.method,
        "url": str(request.url),
        "headers": dict(request.headers),
        "client_host": request.client.host,
        "client_port": request.client.port
    }
    
    # Prepare response headers
    response_headers = {
        "X-Request-Method": request_info["method"],
        "X-Request-URL": request_info["url"],
        "X-Request-Client-Host": request_info["client_host"],
        "X-Request-Client-Port": str(request_info["client_port"])
    }
    
    # Add selected request headers to response headers
    for header_name, header_value in request_info["headers"].items():
        response_headers[f"X-Request-Header-{header_name}"] = header_value
    
    return JSONResponse(
        content={"message": "Request info added to response headers"},
        headers=response_headers
    )

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q, "environment": "development"}