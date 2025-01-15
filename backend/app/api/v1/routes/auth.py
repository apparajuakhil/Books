from fastapi import APIRouter, Depends, HTTPException, Request, status, Form
from sqlalchemy.orm import Session
from app.api.v1.services.auth import authenticate_user
from app.api.dependencies.db import get_db
from app.db.schemas.auth import LoginRequest, TokenResponse
from app.db.schemas.errors import (
    BadRequestError,
    UnauthorizedError,
    InternalServerError,
)
router = APIRouter()

@router.post(
    "/login",
    response_model=TokenResponse,
    responses={
        200: {"description": "Authentication successful. Token returned.", "model": TokenResponse},
        400: {"description": "Invalid request (missing username or password).", "model": BadRequestError},
        500: {"description": "Internal server error.", "model": InternalServerError},
    },
)
async def login(
    request: Request,
    db: Session = Depends(get_db),
    username: str = Form(None),  
    password: str = Form(None),  
):
    """
    Login endpoint to authenticate users.
    Supports both JSON and form data formats for username and password.

    - JSON: {"username": "admin", "password": "admin123"}
    - Form: username=admin&password=admin123
    """
    try:
        # Check Content-Type
        content_type = request.headers.get("Content-Type", "").lower()

        # Handle JSON payload
        if "application/json" in content_type:
            body = await request.json()
            username = body.get("username")
            password = body.get("password")

        # Validate inputs
        if not username or not password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid request. Provide username and password in JSON or form data.",
            )

        # Delegate authentication logic to the service
        token = authenticate_user(username, password)
        return {"access_token": token, "token_type": "bearer"}

    except HTTPException as e:
        # Re-raise HTTP exceptions to propagate to the client
        raise e
    except Exception as e:
        # Catch other exceptions and return a 500 error
        raise HTTPException(
            status_code=500,
            detail="An internal server error occurred.",
        )
