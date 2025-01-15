from sqlalchemy.orm import Session
from backend.app.db.database import SessionLocal

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
