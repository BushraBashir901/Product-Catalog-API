from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
import uuid

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 1. Give each request a unique ID
        request_id = str(uuid.uuid4())
        
        # 2. Remember the start time
        start_time = time.time()
        
        # 3. Print request info
        print(f"[{request_id}] Request: {request.method} {request.url.path}")
        
        # 4. Send request to the route
        response = await call_next(request)
        
        # 5. Calculate how long it took
        duration = time.time() - start_time
        
        # 6. Print response info
        print(f"[{request_id}] Done in {duration:.4f} sec | Status: {response.status_code}")
        
        
        return response