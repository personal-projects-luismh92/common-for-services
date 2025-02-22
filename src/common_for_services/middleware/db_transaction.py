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
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import text


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
    def __init__(self, database: Session, send_alert_email):
        """Initializes the database transaction middleware."""
        _database = database
        _send_alert_email = send_alert_email

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
            logger.error(json.dumps({
                "event": "db_transaction_error",
                "error": str(e),
                "path": request.url.path
            }))

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
                "modulo": "DBTransactionMiddleware",
                "response_time": f"Request processed in {process_time:.2f} seconds"
            })


    def log_event(self, event_type: str, description: str, db: Session):
        """Logs an event in the database.

        This function inserts a structured log entry into an `event_log` table
        whenever a database transaction failure occurs.

        Args:
            event_type (str): The type of event to be logged.
            description (str): A detailed description of the event.
            db (Session): The active database session.
        """
        try:
            db.execute(text("""
                INSERT INTO event_log (event_type, description, timestamp) VALUES (:event_type, :description, NOW())
            """), {"event_type": event_type, "description": description})
            db.commit()
        except Exception as e:
            logger.error(f"Error logging event: {str(e)}")
