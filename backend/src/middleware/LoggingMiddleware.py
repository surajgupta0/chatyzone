from starlette.middleware.base import BaseHTTPMiddleware
import logging
import time
from fastapi import Request

# Logging Configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Custom Logging Middleware
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        logger.info(f"Request: {request.method} {request.url}")

        response = await call_next(request)  # Call the next middleware/route handler

        process_time = time.time() - start_time
        logger.info(f"Response: {response.status_code} (Processed in {process_time:.2f}s)")

        return response