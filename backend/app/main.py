import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from api.v1.routes import books, auth, sse
import logging
from db.database import SessionLocal
from core.openapi import custom_openapi
from fastapi.exceptions import RequestValidationError
from backend.app.db.schemas.errors import ValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

# Initialize the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Books API",
    description="CRUD API for books with JWT authentication",
    version="1.0.0",
)

@app.on_event("startup")
async def startup():
    """
    Runs during application startup. Use this to initialize resources.
    """
    logger.info("Starting up the application...")
    db = SessionLocal()
    try:
        logger.info("Database connection initialized successfully.")
    finally:
        db.close()

@app.on_event("shutdown")
async def shutdown():
    """
    Runs during application shutdown. Use this to clean up resources.
    """
    logger.info("Shutting down the application...")
    logger.info("Resources cleaned up successfully.")

# Example middleware for debugging
@app.middleware("http")
async def log_requests(request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logging.error(f"Error: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500, content={"detail": "An unexpected error occurred."}
        )
    
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Global handler for HTTP exceptions.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Custom exception handler for validation errors.
    """
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors()
        },
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """
    Global handler for unexpected server errors.
    """
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected server error occurred."},
    )

# Include v1 routers
app.include_router(books.router, prefix="/v1/books", tags=["Books"])
app.include_router(auth.router, prefix="/v1/auth", tags=["Authentication"])
app.include_router(sse.router, prefix="/v1/stream", tags=["Real-Time Updates"])

# Apply custom OpenAPI
app.openapi = lambda: custom_openapi(app)