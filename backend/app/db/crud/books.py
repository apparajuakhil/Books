from sqlalchemy.orm import Session
from app.db.models import Book
from app.db.schemas import BookCreate, BookUpdate
from fastapi import HTTPException, status
from datetime import datetime

DATE_FORMAT = "%Y-%m-%d"

def create_book(db: Session, book: BookCreate):
    try:
        book_data = book.dict()
        if book.published_date:
            book_data["published_date"] = book.published_date.strftime(DATE_FORMAT)
        db_book = Book(**book_data)
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book
    except Exception as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))

def get_books(db: Session, skip: int, limit: int):
    books = db.query(Book).offset(skip).limit(limit).all()
    for book in books:
        if book.published_date:
            book.published_date = datetime.strptime(book.published_date, DATE_FORMAT).date()
    return books

def get_book(db: Session, book_id: int):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Book not found")
    if book.published_date:
        book.published_date = datetime.strptime(book.published_date, DATE_FORMAT).date()
    return book

def update_book(db: Session, book_id: int, book: BookUpdate):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Book not found")
    for key, value in book.dict(exclude_unset=True).items():
        if key == "published_date" and value:
            value = value.strftime(DATE_FORMAT)
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return {"detail": "Book deleted"}
