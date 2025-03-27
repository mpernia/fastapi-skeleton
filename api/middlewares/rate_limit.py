import time
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.rate_limit = 100  # requests per minute
        self.window = 60  # seconds
        self.clients = {}

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        client_ip = request.client.host if request.client else "unknown"
        
        # Simple in-memory rate limiting
        # In production, use Redis for distributed rate limiting
        if client_ip in self.clients:
            if len(self.clients[client_ip]) >= self.rate_limit:
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Too many requests"},
                )
            self.clients[client_ip].append(time.time())
            
            # Clean old requests
            self.clients[client_ip] = [
                t for t in self.clients[client_ip]
                if time.time() - t < self.window
            ]
        else:
            self.clients[client_ip] = [time.time()]
        
        return await call_next(request)
