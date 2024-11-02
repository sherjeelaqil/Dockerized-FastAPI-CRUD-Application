# Dockerized-FastAPI-CRUD-Application-
This project is a User Management System built with FastAPI, providing a RESTful API with JWT-based authentication, role-based authorization, and Docker containerization. This API enables CRUD operations on user data and includes optional features like rate limiting and automated testing.


## 📋 Features Checklist

### 📦 CRUD Operations
  - [X] Create user endpoint
  - [X] Read user(s) endpoint
  - [X] Update user endpoint
  - [X] Delete user endpoint
  - [X] User model with required fields
    - [X] id (unique identifier)
    - [X] username (unique, required)
    - [X] email (unique, required)
    - [X] password (required)
    - [X] role (admin/user)

### 🔐 Authentication
  - [X] JWT token-based authentication
  - [X] Login endpoint implementation
  - [X] Password hashing
  - [X] Secure token generation and validation

### 👮 Authorization
  - [X] Role-based access control
    - [X] Admin role permissions
    - [X] User role permissions
  - [X] Authorization middleware
  - [X] Protected route implementation
  - [X] User-specific access restrictions

### 🛣️ API Endpoints
  - [X] POST /register
  - [X] POST /login
  - [X] GET /users
  - [X] GET /users/{id}
  - [X] PUT /users/{id}
  - [X] DELETE /users/{id}

### 🐳 Docker Setup
  - [X] Dockerfile creation
  - [X] Docker Compose configuration
  - [X] Database container setup
  - [X] Environment configuration
  - [X] Single command deployment (`docker-compose up`)

### ✨ Best Practices Implementation
  - [X] Environment configuration
    - [X] .env file setup
    - [X] Configuration validation
  - [X] Dependency injection
  - [X] Error handling
    - [X] Custom error responses
    - [X] Error middleware
  - [X] Code documentation
    - [X] Function docstrings
    - [X] Module documentation
  - [X] Logging system
    - [X] User creation logs
    - [X] Authentication logs
    - [X] Error logs
  - [X] Clean code architecture
    - [X] Proper file structure
    - [X] Code organization
    - [X] Naming conventions

### 📚 Documentation
  - [X] API documentation
    - [X] Swagger UI
    - [X] ReDoc setup
  - [X] Setup instructions
  - [X] Architecture explanation
  - [X] API usage examples
  - [X] Environment variables documentation

### 🎯 Optional Features
  - [X] Testing
    - [X] Unit tests setup
    - [X] Integration tests setup
    - [X] Test coverage reports
  - [X] API rate limiting
    - [X] Rate limit middleware
    - [X] Configuration options


## 🚀 Quick Start

1. Clone the repository
```bash
git clone <repository-url>
cd <project-directory>
```

2. Set up environment variables
```bash
cp .env.example .env
# Edit .env file with your configurations
```

3. Start the application using Docker
```bash
docker-compose up -d
```

4. Access the application:
- API: http://localhost:8000
- Documentation: http://localhost:8000/docs
- Alternative Documentation: http://localhost:8000/redoc

## 🔧 Development Setup

### Prerequisites
- Python 3.8+
- Docker and Docker Compose
- SQLite

### Local Development
1. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run migrations
```bash
alembic upgrade head
```

4. Start the development server
```bash
uvicorn app.main:app --reload
```

### Running Unit tests/Coverage tests
1. Unit tests
```bash
pytest -v
```

2. Coverage tests
```bash
pytest tests/ -v --cov=app
```

## 📝 API Documentation

### Authentication Endpoints

#### Register User
```bash
curl -X POST 'http://localhost:8000/register' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_TOKEN_HERE' \
  -d '{
    "email": "test2@example.com",
    "password": "test2",
    "role": "user",
    "username": "test2"
  }'
```

#### Login
```bash
curl -X POST 'http://localhost:8000/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "username": "test",
    "password": "strongpass123"
  }'
```

### User Management Endpoints

> **Note**: All endpoints require JWT authentication. Include the token in the Authorization header:
```bash
Authorization: Bearer YOUR_JWT_TOKEN_HERE
```

#### Get All Users (Admin Only)
```bash
curl -X GET 'http://localhost:8000/users' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_JWT_TOKEN_HERE'
```

#### Get User by ID
```bash
curl -X GET 'http://localhost:8000/users/2' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_JWT_TOKEN_HERE'
```

#### Update User (Admin Only)
```bash
curl -X PUT 'http://localhost:8000/users/2' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_JWT_TOKEN_HERE' \
  -d '{
    "username": "test",
    "email": "test@example.com",
    "password": "strongpass123",
    "role": "admin"
  }'
```

#### Delete User (Admin Only)
```bash
curl -X DELETE 'http://localhost:8000/users/2' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_JWT_TOKEN_HERE'

## 🏗️ Project Structure

```
.
|   docker-compose.yml
|   Dockerfile
|   README.md
|   requirements.txt
|   
+---app
|   |   auth.py
|   |   dependencies.py
|   |   main.py
|   |   __init__.py
|   |   
|   +---common
|   |       app.log
|   |       config.py
|   |       database.py
|   |       init_db.py
|   |       limiter.py
|   |       logging_config.py
|   |       
|   +---crud
|   |       crud.py
|   |       
|   +---middlewares
|   |       admin.py
|   |       
|   +---models
|   |       users_models.py
|   |       
|   +---routes
|   |       users_routes.py
|   |       
|   \---schemas
|           token.py
|           users_schemas.py
|           
\---tests
        conftest.py
        test_auth.py
        test_dependencies.py
        test_users_routes.py
        __init__.py
```

## ⚙️ Environment Variables

```env
# Authentication
SECRET_KEY=your_secret_key_here
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
RATE_LIMIT_MAX_REQUESTS=5
RATE_LIMIT_WINDOW=60

# Database
DATABASE_URL=sqlite:///./test.db
```
