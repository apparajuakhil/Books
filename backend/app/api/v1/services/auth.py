from fastapi import HTTPException, status
from backend.app.core.security import verify_password, create_access_token, hash_password
from backend.app.core.sse import add_event  # Import the SSE event function

# Mock user database
fake_users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": hash_password("admin123"),  
    }
}

def authenticate_user(username: str, password: str) -> str:
    """
    Authenticates a user and returns a JWT token.

    :param username: The username of the user.
    :param password: The plain text password of the user.
    :return: A JWT token if authentication is successful.
    :raises HTTPException: If authentication fails.
    """
    user = fake_users_db.get(username)
    if not user or not verify_password(password, user["hashed_password"]):
        add_event(
            event_type="auth-failed",
            message=f"Login failed for username: {username}",
            data={"username": username}
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    add_event(
        event_type="auth-success",
        message=f"User logged in successfully: {username}",
        data={"username": username}
    )
    
    return create_access_token({"sub": username})
