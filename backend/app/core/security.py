from datetime import datetime, timedelta
from jose import jwt, JWTError, ExpiredSignatureError
from passlib.context import CryptContext
from app.core.config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.sse import add_event  # Import add_event for SSE

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2PasswordBearer for extracting the token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain password against a hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    """
    Hashes a plain text password.
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Creates a JWT token with an expiration time.

    :param data: Data to encode in the token.
    :param expires_delta: Optional timedelta for token expiration.
    :return: Encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Verifies the validity of a JWT token.

    :param token: JWT token from the Authorization header.
    :return: Decoded token payload if valid.
    :raises HTTPException: If the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except ExpiredSignatureError:
        # Trigger event for expired token
        add_event(
            event_type="auth-token-expired",
            message="Token has expired",
            data={}
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )
