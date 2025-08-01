from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

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