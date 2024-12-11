# Flask Sum API

A Flask-based REST API that manages and filters arithmetic sums. This API allows you to store sums of two numbers and retrieve them based on their results.

## Features

- Add new sums via POST request
- Retrieve all stored sums
- Filter sums by their result value
- SQLite for local development
- PostgreSQL support for production
- Comprehensive test suite

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

The application uses SQLite by default for local development. For production, set the `DATABASE_URL` environment variable to your PostgreSQL connection string:

```bash
# Local development (default)
# Uses SQLite: sqlite:///sums.db

# Production
export DATABASE_URL=postgresql://username:password@host:port/dbname
```

## API Endpoints

### POST /sum
Add a new sum.

Request body:
```json
{
    "num1": 2,
    "num2": 2
}
```

Response:
```json
{
    "id": 1,
    "num1": 2,
    "num2": 2,
    "result": 4
}
```

### GET /sum
Retrieve all stored sums.

Response:
```json
[
    {
        "id": 1,
        "num1": 2,
        "num2": 2,
        "result": 4
    },
    {
        "id": 2,
        "num1": 3,
        "num2": 1,
        "result": 4
    }
]
```

### GET /sum/result/<int>
Retrieve sums filtered by result.

Example: `/sum/result/4`

Response:
```json
[
    {
        "id": 1,
        "num1": 2,
        "num2": 2,
        "result": 4
    },
    {
        "id": 2,
        "num1": 3,
        "num2": 1,
        "result": 4
    }
]
```

## Running Tests

Run the test suite using pytest:

```bash
python -m pytest test_app.py -v
```

The tests use an in-memory SQLite database and cover:
- Adding new sums
- Filtering sums by result
- Handling non-existent results

## Deployment

This application is configured for deployment on Render.

1. Create a new Web Service on Render
2. Link your GitHub repository
3. Configure the following:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Environment Variables:
     - `DATABASE_URL`: Your PostgreSQL database URL
     - `PYTHON_VERSION`: 3.12.6

## Development

To run the application locally:

```bash
python app.py
```

The server will start at `http://localhost:5000`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
