from pydantic import BaseModel
from typing import Optional, List
from datetime import date


class BookBase(BaseModel):
    title: str
    author: str
    published_date: Optional[date] = None
    summary: Optional[str] = None
    genre: str


class BookCreate(BookBase):
    """
    Schema for creating a new book.
    """
    class Config:
        json_schema_extra = {
            "example": {
                "title": "To Kill a Mockingbird",
                "author": "Harper Lee",
                "published_date": "1960-07-11",
                "summary": "A novel about racism and injustice.",
                "genre": "Fiction"
            }
        }


class BookPut(BookBase):
    """
    Schema for updating an entire book record.
    """
    class Config:
        json_schema_extra = {
            "example": {
                "title": "1984",
                "author": "George Orwell",
                "published_date": "1949-06-08",
                "summary": "A dystopian novel about a totalitarian regime.",
                "genre": "Dystopian Fiction"
            }
        }


class BookPatch(BaseModel):
    """
    Schema for partially updating a book record.
    """
    title: Optional[str] = None
    author: Optional[str] = None
    published_date: Optional[date] = None
    summary: Optional[str] = None
    genre: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Animal Farm",
                "summary": "A satirical novella about farm animals rebelling against humans."
            }
        }


class Book(BookBase):
    """
    Schema representing a complete book with an ID.
    """
    id: int

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "published_date": "1925-04-10",
                "summary": "A novel about the American dream.",
                "genre": "Fiction"
            }
        }


# Response schemas
class BooksResponse(BaseModel):
    """
    Response schema for retrieving a list of books.
    """
    items: List[Book]
    total: int
    skip: int
    limit: int

    class Config:
        json_schema_extra = {
            "example": {
                "items": [
                    {
                        "id": 1,
                        "title": "The Great Gatsby",
                        "author": "F. Scott Fitzgerald",
                        "published_date": "1925-04-10",
                        "summary": "A novel about the American dream.",
                        "genre": "Fiction"
                    },
                    {
                        "id": 2,
                        "title": "To Kill a Mockingbird",
                        "author": "Harper Lee",
                        "published_date": "1960-07-11",
                        "summary": "A novel about racism and injustice.",
                        "genre": "Fiction"
                    }
                ],
                "total": 2,
                "skip": 0,
                "limit": 10
            }
        }


class BookCreatedResponse(BaseModel):
    """
    Response schema for successfully created book.
    """
    book: Book

    class Config:
        json_schema_extra = {
            "example": {
                "book": {
                    "id": 3,
                    "title": "1984",
                    "author": "George Orwell",
                    "published_date": "1949-06-08",
                    "summary": "A dystopian novel about a totalitarian regime.",
                    "genre": "Dystopian Fiction"
                }
            }
        }


class SuccessResponse(BaseModel):
    """
    Generic success response model for operations like DELETE.
    """
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Book deleted successfully"
            }
        }


class ErrorResponse(BaseModel):
    """
    Generic error response model.
    """
    detail: str

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Book with ID 123 not found"
            }
        }
