"""
Authentication Middleware Module.

This module provides JWT-based authentication middleware for FastAPI applications.
It ensures that all incoming requests include a valid JWT token before proceeding.

Environment Variables:
    JWT_SECRET (str): The secret key used to sign and verify JWT tokens (default: "mysecret").

Classes:
    AuthenticationMiddleware: Middleware that enforces authentication using JWT tokens.

Attributes:
    SECRET_KEY (str): The secret key for decoding JWT tokens.

Exceptions:
    HTTPException (401): Raised when the token is expired or invalid.

"""
from fastapi import Request, HTTPException, Security
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.security import HTTPBearer
import jwt
import os

# Secret key for JWT validation, loaded from environment variables
SECRET_KEY = os.getenv("JWT_SECRET", "mysecret")

class AuthenticationMiddleware(BaseHTTPMiddleware):
    """Middleware for authentication using JWT tokens.

    This middleware intercepts incoming requests and checks for a valid JWT token 
    in the Authorization header. If valid, the decoded payload is stored in `request.state.user`.

    Raises:
        HTTPException (401): If the token is expired or invalid.
    """

    async def dispatch(self, request: Request, call_next):
        """Intercepts and processes incoming requests to enforce authentication.

        The function retrieves the Authorization token from the request, decodes it using the
        secret key, and adds the user payload to `request.state.user`. If the token is missing,
        expired, or invalid, an HTTP 401 Unauthorized error is raised.

        Args:
            request (Request): The incoming HTTP request.
            call_next (Callable): The next middleware or route handler.

        Returns:
            Response: The HTTP response from the next middleware or endpoint.
        """
        auth = HTTPBearer()
        credentials = await auth(request)

        try:
            payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
            request.state.user = payload  # Store user data in request state
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

        return await call_next(request)
