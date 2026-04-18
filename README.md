# Rocky Jam Backend

A FastAPI-based backend service for managing music compositions, users, and authentication. Built with SQLModel for database interactions and PostgreSQL as the database.

## Features

- **User Management**: Register, login, and manage user accounts with JWT authentication.
- **Composition Management**: Create, read, update, and delete music compositions.
- **Section and Chord Handling**: Manage sections within compositions and chords within sections.
- **Database Integration**: Uses PostgreSQL with SQLModel for ORM.
- **API Documentation**: Automatic API docs via FastAPI (Swagger UI at `/docs`).

## Prerequisites

- Python 3.8+
- PostgreSQL database
- Virtual environment (recommended)

## Installation

1. **Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the root directory with the following variables:
   ```
   PG_HOST=localhost
   PG_PORT=5432
   PG_USER=your_db_user
   PG_PASSWORD=your_db_password
   PG_DATABASE=your_db_name

   SECRET_KEY=your_secret_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

4. **Set up the database**:
   - Ensure PostgreSQL is running.
   - Create a database matching `PG_DATABASE`.
   - The app will automatically create tables on startup via the lifespan event.

## Running the Application

1. **Start the server**:
   ```bash
   fastapi dev
   ```
   Or with uvicorn:
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Access the API**:
   - API docs: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc
