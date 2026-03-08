from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from openai import APIError, RateLimitError, AuthenticationError
import structlog

logger = structlog.get_logger()


async def global_exception_handler(request: Request, exc: Exception):
    """Handle all unhandled exceptions."""
    logger.error(
        "unhandled_exception",
        path=request.url.path,
        method=request.method,
        error=str(exc),
        error_type=type(exc).__name__
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "detail": "An unexpected error occurred. Please try again later.",
            "request_id": request.headers.get("X-Request-ID")
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors."""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"] if loc != "body"),
            "message": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation error",
            "detail": errors
        }
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handle database errors."""
    logger.error(
        "database_error",
        path=request.url.path,
        error=str(exc)
    )
    
    error_detail = "A database error occurred. Please try again later."
    
    if "unique constraint" in str(exc).lower():
        error_detail = "A record with this value already exists."
    elif "foreign key constraint" in str(exc).lower():
        error_detail = "Referenced record does not exist."
    elif "connection" in str(exc).lower():
        error_detail = "Database connection error. Please try again later."
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Database error",
            "detail": error_detail
        }
    )


async def value_error_handler(request: Request, exc: ValueError):
    """Handle value errors."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Bad request",
            "detail": str(exc)
        }
    )


async def openai_api_error_handler(request: Request, exc: APIError):
    """Handle OpenAI API errors."""
    logger.error(
        "openai_api_error",
        path=request.url.path,
        error=str(exc),
        type=type(exc).__name__
    )
    
    if isinstance(exc, RateLimitError):
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={
                "error": "Rate limit exceeded",
                "detail": "Too many requests to AI service. Please wait and try again."
            }
        )
    elif isinstance(exc, AuthenticationError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "error": "API authentication failed",
                "detail": "Invalid API key. Please check your configuration."
            }
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content={
                "error": "AI service error",
                "detail": "Failed to communicate with AI service. Please try again."
            }
        )


async def http_exception_handler(request: Request, exc):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )
