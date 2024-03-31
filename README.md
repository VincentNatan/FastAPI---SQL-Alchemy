# FastAPI User Management API

This is a FastAPI project for managing users, implementing CRUD operations with SQLAlchemy.

## Installation

To run this project locally, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/fastapi-user-management.git
   cd fastapi-user-management

2. Install Depedencies

   ```bash
   poetry run pytest

4. Setup Database

   ```bash
   python database.py

## Usage

1. Start the FastAPI server:

   ```bash
   poetry run uvicorn main:app --reload
   
3. Open your web browser or use a tool like Postman to interact with the API endpoints.
4. Use the following endpoints to manage users:

   - **Create User**: POST /api/create/
   - **Get User by ID**: GET /api/users/{user_id}
   - **Update User**: PUT /api/update/{user_id}
   - **Delete User**: DELETE /api/delete/{user_id}

## Testing

You can run the unit tests using pytest.
