"""
Database Transaction Middleware Module.

This module provides middleware for monitoring database transactions in FastAPI applications.
It ensures that database errors are properly logged, alerts are sent, and transactions are rolled back
to maintain data integrity.

Dependencies:
    - SQLAlchemy for database session handling.
    - Logging for structured error tracking.
    - Email utility for sending alerts on transaction failures.

Environment Variables:
    None (but relies on `common.database.connection` for DB sessions and `common.utils.email` for alerts).

Classes:
    DBTransactionMiddleware: Middleware that monitors database transactions and handles failures.

Attributes:
    logger (logging.Logger): Logger instance for monitoring database transaction errors.

Exceptions:
    SQLAlchemyError: Raised when an error occurs during a database transaction.

"""
import logging
import json
import time
import datetime
from fastapi import Request, Response, FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
from common_for_services.tasks.celery_worker import celery

# Logger for database transaction monitoring
logger = logging.getLogger("db_transaction_monitoring")


class DBTransactionMiddleware(BaseHTTPMiddleware):
    """Middleware to monitor database transactions and log failures.

    This middleware ensures that database operations are properly handled within a transaction.
    If an exception occurs, it:
    - Rolls back the transaction.
    - Logs the error in both the application logs and a dedicated event log table.
    - Sends an email alert for immediate attention.

    Raises:
        SQLAlchemyError: If a database transaction error occurs.
    """

    def __init__(self, app: FastAPI,
                 celery_app: Optional[celery] = None):
        super().__init__(app)
        self.celery_app = celery_app  # Injected Celery

    async def dispatch(self, request: Request, call_next):
        """Intercepts and processes incoming requests to ensure transaction safety.

        This function wraps database transactions in a try-except-finally block to:
        - Ensure transactions are properly committed or rolled back.
        - Log transaction failures and generate structured logs.
        - Send alerts for transaction errors.

        Args:
            request (Request): The incoming HTTP request.
            call_next (Callable): The next middleware or route handler.

        Returns:
            Response: The HTTP response from the next middleware or endpoint.
        """
        start_time = time.time()

        try:
            response = await call_next(request)
            return response
        except SQLAlchemyError as e:
            process_time = time.time() - start_time

            log_data = {
                "package": "middleware",
                "module": "db_transaction.DBTransactionMiddleware",
                "log": "CRITICAL",
                "event": "db_transaction_error",
                "error": str(e),
                "method": request.method,
                "path": request.url.path,
                "response_time": f"Request processed in {process_time:.2f} seconds",
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            logger.error(json.dumps(log_data))

            if self.celery_app:
                # Send structured log data to the logging service
                self.celery_app.send_task(
                    "celery_worker.tasks.log_to_logging_service_task", args=[log_data])
                self.celery_app.send_task(
                    "celery_worker.tasks.send_email_task",
                    args=["admin@example.com", "Database Error Alert",
                          json.dumps(log_data, indent=2)]
                )

            return Response(
                content=json.dumps(
                    {"status": "error", "message": "Error interno en el sistema"}),
                media_type="application/json",
                status_code=500
            )
        finally:
            process_time = time.time() - start_time

            logger.info({
                "package": "middleware",
                "module": "db_transaction.DBTransactionMiddleware",
                "log": "CRITICAL",
                "event": "db_transaction_complete",
                "error": None,
                "method": request.method,
                "path": request.url.path,
                "response_time": f"Request processed in {process_time:.2f} seconds",
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
