import time
from typing import Callable

import structlog
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = structlog.get_logger()

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        response = await call_next(request)
        
        process_time = (time.time() - start_time) * 1000
        log_dict = {
            "request": {
                "method": request.method,
                "path": request.url.path,
                "client_ip": request.client.host if request.client else None,
            },
            "response": {
                "status_code": response.status_code,
                "process_time_ms": process_time,
            },
        }
        
        logger.info("request processed", **log_dict)
        
        return response
