"""
Logging Middleware Module.

This module provides middleware for structured logging of incoming HTTP requests in FastAPI applications.
It captures details such as request method, path, response status, and processing time.

Dependencies:
    - Logging for structured request tracking.
    - FastAPI Request and Starlette middleware for request handling.

Environment Variables:
    None.

Classes:
    LoggingMiddleware: Middleware that logs incoming requests and response details.

Attributes:
    logger (logging.Logger): Logger instance for request monitoring.

"""
import logging
import time
import datetime
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

# Logger for request monitoring
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("request_logger")

class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for structured request logging.

    This middleware captures essential request and response details, including:
    - HTTP method (GET, POST, etc.).
    - Request path.
    - Client IP address.
    - Response status code.
    - Processing time of the request.

    The structured logs help in monitoring API performance and diagnosing issues.

        Example log output:
        {
            "event": "http_request",
            "method": "GET",
            "path": "/health",
            "client_ip": "192.168.1.1",
            "status_code": 200,
            "response_time": "0.02s"
        }
    """

    async def dispatch(self, request: Request, call_next):
        """Intercepts and logs details of incoming HTTP requests.

        This function records:
        - The start time of the request.
        - The HTTP method and path.
        - The status code and response time after processing.

        Args:
            request (Request): The incoming HTTP request.
            call_next (Callable): The next middleware or route handler.

        Returns:
            Response: The HTTP response from the next middleware or endpoint.
        """
        start_time = time.time()  # Start request timer
        response = await call_next(request)  # Process request
        process_time = time.time() - start_time  # Calculate response time
        if request.client:
            client_ip = request.client.host  # Extract client IP address

        # Log structured request details
        logger.info({
            "package": "middleware",
            "modulo": "logging.LoggingMiddleware",
            "event": "http/https_request",
            "method": request.method,
            "path": request.url.path,
            "client_ip": client_ip,
            "status_code": response.status_code,
            "response_time": f"{process_time:.2f}s",
            "event_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        return response