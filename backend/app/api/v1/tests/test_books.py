from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_book():
    # Login to get the token
    login_response = client.post(
        "/v1/auth/login",
        json={"username": "admin", "password": "admin123"}
    )
    token = login_response.json()["access_token"]

    # Create a book
    response = client.post(
        "/v1/books/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Test Book",
            "author": "Author Name",
            "published_date": "2023-01-01",
            "summary": "This is a test book.",
            "genre": "Fiction"
        }
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Book"

def test_get_books():
    response = client.get("/v1/books/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_book_by_id():
    response = client.get("/v1/books/1")  # Assuming a book with ID 1 exists
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_update_book():
    response = client.put(
        "/v1/books/1",
        json={
            "title": "Updated Book Title",
            "author": "Updated Author",
            "published_date": "2023-06-01",
            "summary": "Updated summary.",
            "genre": "Non-Fiction"
        }
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Book Title"

def test_delete_book():
    response = client.delete("/v1/books/1")
    assert response.status_code == 200
    assert response.json() == {"detail": "Book deleted"}
