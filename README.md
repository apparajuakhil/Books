# Books API

The **Books API** is a FastAPI-based application that allows users to manage a collection of books. This includes creating, reading, updating, and deleting books from a database. The API is deployed on Heroku, and Swagger documentation is available for easy testing and exploration.

## API Documentation

Explore the API using Swagger UI:  
[Books API Documentation](https://booksbackend-7f60395de01c.herokuapp.com/docs)

---

## Features

- CRUD operations for managing books.
- Token-based authentication for secured endpoints.
- SQLite database for persistent data storage.
- Automatic API documentation with Swagger.
- Deployed and accessible on Heroku.

---

## Steps to run:

1. Clone the repository:
   git clone https://github.com/apparajuakhil/Books.git
   cd books/backend
2. Create and activate a virtual environment:
   python3 -m venv venv
   source venv/bin/activate
3. Install dependencies:
   pip install -r requirements.txt
4. Set up the .env file: Create a .env file in the root directory with the following content:
   DATABASE_URL=sqlite:///../books.db
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
5. Run database migrations
6. Start the server:
   uvicorn backend.app.main:app --reload

## API Endpoints

### Authentication

- POST /v1/auth/login: Authenticate user and get a token.

### Books

- POST /v1/books/: Create a new book.
- GET /v1/books/: Retrieve a paginated list of books.
- GET /v1/books/{book_id}: Retrieve a specific book by ID.
- PUT /v1/books/{book_id}: Update an existing book.
- PATCH /v1/books/{book_id}: Partially update a book.
- DELETE /v1/books/{book_id}: Delete a book by ID.

### Streaming

- GET /v1/stream/: Open an SSE connection to receive real-time updates.

## Tech Stack

The **Books API** is built using the following technologies:

### Backend

- **FastAPI**: High-performance web framework for building APIs with Python 3.10+.
- **SQLite**: Lightweight, file-based database for storing application data.
- **SQLAlchemy**: ORM for database interactions and migrations.
- **Pydantic**: Data validation and settings management.
- **Uvicorn**: ASGI server for running FastAPI applications.

### Streaming

- **Server-Sent Events (SSE)**: Used for real-time data streaming to clients.

### Authentication & Security

- **OAuth2**: Token-based authentication using FastAPI's `OAuth2PasswordBearer`.
- **JWT**: JSON Web Tokens for secure access token generation.
- **Passlib**: Password hashing for user authentication.

### Deployment

- **Heroku**: Cloud platform for hosting and deployment.
  - Runtime: `python-3.10.x`
  - Buildpacks: Python buildpack for dependency management.
- **Gunicorn**: WSGI server used in production.

### Testing

- **Pytest**: Framework for writing and running tests.
- **Postman**: API testing and debugging tool.

### Development Tools

- **Python Virtual Environment (venv)**: Isolated environment for dependencies.
- **Prettier**: Code formatter for consistent code style.
- **VS Code**: Code editor with FastAPI plugins for linting and debugging.

---

## Debugging Tips

1. To enable debug logs, set the environment variable:
   LOG_LEVEL=debug
2. Ensure the database file (books.db) is correctly located and accessible.
