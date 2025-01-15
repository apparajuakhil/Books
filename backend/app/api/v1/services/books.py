from sqlalchemy.orm import Session
from app.db.models import Book
from app.db.schemas.books import BookCreate, BookPut, BookPatch
from fastapi import HTTPException, status
from datetime import datetime, date
from app.core.sse import add_event

DATE_FORMAT = "%Y-%m-%d"

class BookService:
    def create_book(self, db: Session, book: BookCreate):
        book_data = book.dict()
        if book.published_date:
            book_data["published_date"] = book.published_date.strftime(DATE_FORMAT)
        try:
            db_book = Book(**book_data)
            db.add(db_book)
            db.commit()
            db.refresh(db_book)
            add_event(
                event_type="book-created",
                message=f"Book created: {db_book.title}",
                data={"id": db_book.id, "title": db_book.title, "author": db_book.author},
            )
            return db_book
        except Exception as e:
            db.rollback()
            add_event(
                event_type="error",
                message="Failed to create book",
                data={"error": str(e)},
            )
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()  

    def get_books(self, db: Session, skip: int, limit: int):
        books = db.query(Book).offset(skip).limit(limit).all()
        total = db.query(Book).count()
        for book in books:
            if book.published_date:
                book.published_date = datetime.strptime(book.published_date, DATE_FORMAT).date()
        return books, total

    def get_book(self, db: Session, book_id: int):
        try:
            book = db.query(Book).filter(Book.id == book_id).first()
            if not book:
                add_event(
                    event_type="error",
                    message=f"Book with ID {book_id} not found",
                    data={"id": book_id},
                )
                raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Book with ID {book_id} not found")
            if book.published_date:
                book.published_date = datetime.strptime(book.published_date, DATE_FORMAT).date()
            return book
        except Exception as e:
            add_event(
                event_type="error",
                message=f"Error retrieving book with ID {book_id}",
                data={"id": book_id, "error": str(e)},
            )
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def update_book(self, db: Session, book_id: int, book: BookPut):
        db_book = db.query(Book).filter(Book.id == book_id).first()
        if not db_book:
            add_event(
                event_type="error",
                message=f"Book with ID {book_id} not found",
                data={"id": book_id},
            )
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Book with ID {book_id} not found")
        try:
            for key, value in book.dict(exclude_unset=True).items():
                if key == "published_date" and isinstance(value, date):
                    value = value.strftime(DATE_FORMAT)
                setattr(db_book, key, value)
            db.commit()
            db.refresh(db_book)
            add_event(
                event_type="book-updated",
                message=f"Book updated: {db_book.title}",
                data={"id": db_book.id, "title": db_book.title, "author": db_book.author},
            )
            return db_book
        except Exception as e:
            db.rollback()
            add_event(
                event_type="error",
                message=f"Failed to update book with ID {book_id}",
                data={"id": book_id, "error": str(e)},
            )
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close() 

    def update_book_partially(self, db: Session, book_id: int, book: BookPatch):
        db_book = db.query(Book).filter(Book.id == book_id).first()
        if not db_book:
            add_event(
                event_type="error",
                message=f"Book with ID {book_id} not found",
                data={"id": book_id},
            )
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Book with ID {book_id} not found")
        try:
            for key, value in book.dict(exclude_unset=True).items():
                if key == "published_date" and isinstance(value, date):
                    value = value.strftime(DATE_FORMAT)
                setattr(db_book, key, value)
            db.commit()
            db.refresh(db_book)
            add_event(
                event_type="book-partially-updated",
                message=f"Book partially updated: {db_book.title}",
                data={"id": db_book.id, "title": db_book.title},
            )
            return db_book
        except Exception as e:
            db.rollback()
            add_event(
                event_type="error",
                message=f"Failed to partially update book with ID {book_id}",
                data={"id": book_id, "error": str(e)},
            )
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close() 

    def delete_book(self, db: Session, book_id: int):
        db_book = db.query(Book).filter(Book.id == book_id).first()
        if not db_book:
            add_event(
                event_type="error",
                message=f"Book with ID {book_id} not found",
                data={"id": book_id},
            )
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Book with ID {book_id} not found")
        try:
            db.delete(db_book)
            db.commit()
            add_event(
                event_type="book-deleted",
                message=f"Book deleted with ID {book_id}",
                data={"id": book_id},
            )
            return {"detail": "Book deleted"}
        except Exception as e:
            db.rollback()
            add_event(
                event_type="error",
                message=f"Failed to delete book with ID {book_id}",
                data={"id": book_id, "error": str(e)},
            )
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close() 


book_service = BookService()
