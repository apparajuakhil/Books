from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.db.schemas.books import Book, BookCreate, BookPut, BookPatch, BooksResponse, BookCreatedResponse, SuccessResponse
from backend.app.db.schemas.errors import (
    BadRequestError,
    UnauthorizedError,
    NotFoundError,
    ValidationError,
    InternalServerError,
)
from backend.app.api.dependencies.db import get_db
from backend.app.core.security import verify_access_token
from backend.app.api.v1.services.books import book_service

# Global dependency to enforce token validation on all endpoints
router = APIRouter(dependencies=[Depends(verify_access_token)])

@router.post(
    "/",
    response_model=BookCreatedResponse,
    responses={
        200: {"description": "Book successfully created.", "model": BookCreatedResponse},
        400: {"description": "Bad Request (Malformed body or headers)", "model": BadRequestError},
        401: {"description": "Unauthorized", "model": UnauthorizedError},
        422: {"description": "Invalid input", "model": ValidationError},
        500: {"description": "Internal Server Error", "model": InternalServerError},
    },
)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """
    Create a new book.
    """
    try:
        created_book = book_service.create_book(db, book)
        return {"book": created_book}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An internal server error occurred."
        )

@router.get(
    "/",
    response_model=BooksResponse,
    responses={
        200: {"description": "List of books retrieved successfully.", "model": BooksResponse},
        400: {"description": "Bad Request (Invalid query parameters)", "model": BadRequestError},
        401: {"description": "Unauthorized", "model": UnauthorizedError},
        500: {"description": "Internal Server Error", "model": InternalServerError},
    },
)
def get_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieve a paginated list of books.
    """
    if skip < 0 or limit < 1:
        raise HTTPException(
            status_code=400,
            detail="Query parameters 'skip' must be >= 0 and 'limit' must be > 0."
        )
    try:
        books, total = book_service.get_books(db, skip, limit)
        return {
            "items": books,
            "total": total,
            "skip": skip,
            "limit": limit
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An internal server error occurred."
        )

@router.get(
    "/{book_id}",
    response_model=Book,
    responses={
        200: {"description": "Book retrieved successfully.", "model": Book},
        400: {"description": "Bad Request (Invalid book ID)", "model": BadRequestError},
        401: {"description": "Unauthorized", "model": UnauthorizedError},
        404: {"description": "Book not found", "model": NotFoundError},
        500: {"description": "Internal Server Error", "model": InternalServerError},
    },
)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a book by its ID.
    """
    if book_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Book ID must be a positive integer."
        )
    try:
        return book_service.get_book(db, book_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An internal server error occurred."
        )

@router.put(
    "/{book_id}",
    response_model=Book,
    responses={
        200: {"description": "Book updated successfully.", "model": Book},
        400: {"description": "Bad Request (Malformed body or headers)", "model": BadRequestError},
        401: {"description": "Unauthorized", "model": UnauthorizedError},
        404: {"description": "Book not found", "model": NotFoundError},
        422: {"description": "Invalid input", "model": ValidationError},
        500: {"description": "Internal Server Error", "model": InternalServerError},
    },
)
def update_book(book_id: int, book: BookPut, db: Session = Depends(get_db)):
    """
    Update an existing book.
    """
    try:
        return book_service.update_book(db, book_id, book)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An internal server error occurred."
        )

@router.patch(
    "/{book_id}",
    response_model=Book,
    responses={
        200: {"description": "Book partially updated successfully.", "model": Book},
        400: {"description": "Bad Request (Malformed body or headers)", "model": BadRequestError},
        401: {"description": "Unauthorized", "model": UnauthorizedError},
        404: {"description": "Book not found", "model": NotFoundError},
        422: {"description": "Invalid input", "model": ValidationError},
        500: {"description": "Internal Server Error", "model": InternalServerError},
    },
)
def update_book_partially(book_id: int, book_update: BookPatch, db: Session = Depends(get_db)):
    """
    Partially update an existing book.
    """
    try:
        return book_service.update_book_partially(db, book_id, book_update)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An internal server error occurred."
        )

@router.delete(
    "/{book_id}",
    response_model=SuccessResponse,
    responses={
        200: {"description": "Book deleted successfully.", "model": SuccessResponse},
        400: {"description": "Bad Request (Invalid book ID)", "model": BadRequestError},
        401: {"description": "Unauthorized", "model": UnauthorizedError},
        404: {"description": "Book not found", "model": NotFoundError},
        500: {"description": "Internal Server Error", "model": InternalServerError},
    },
)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    Delete a book by its ID.
    """
    if book_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Book ID must be a positive integer."
        )
    try:
        book_service.delete_book(db, book_id)
        return {"message": "Book deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An internal server error occurred."
        )
