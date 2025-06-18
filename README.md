# Sample FastAPI Blog API

This is a sample FastAPI application for a blog, demonstrating a multi-file structure with routers and Pydantic models.

## Setup

1.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

To run the FastAPI application, use Uvicorn:

```bash
uvicorn app.main:app --reload
```

The application will typically be available at `http://127.0.0.1:8000`.

## API Endpoints

The API routes are prefixed with `/api`.

### Posts

*   **Create a new post:**
    *   `POST /api/posts/`
    *   Request body (JSON):
        ```json
        {
          "title": "My First Blog Post",
          "content": "This is the content of my first blog post."
        }
        ```
    *   Example using `curl`:
        ```bash
        curl -X POST "http://127.0.0.1:8000/api/posts/" -H "Content-Type: application/json" -d '{"title": "My First Post", "content": "Hello world!"}'
        ```

*   **Get all posts:**
    *   `GET /api/posts/`
    *   Example using `curl`:
        ```bash
        curl -X GET "http://127.0.0.1:8000/api/posts/"
        ```

*   **Get a specific post by ID:**
    *   `GET /api/posts/{post_id}`
    *   Example using `curl` (for post with ID 1):
        ```bash
        curl -X GET "http://127.0.0.1:8000/api/posts/1"
        ```

You can also access the interactive API documentation (Swagger UI) provided by FastAPI at `http://127.0.0.1:8000/docs` and the alternative ReDoc documentation at `http://127.0.0.1:8000/redoc` when the application is running.
