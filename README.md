# Dockerized-FastAPI-CRUD-Application-
This project is a User Management System built with FastAPI, providing a RESTful API with JWT-based authentication, role-based authorization, and Docker containerization. This API enables CRUD operations on user data and includes optional features like rate limiting and automated testing.


## 📋 Features Checklist

- [ ] **CRUD Operations**
  - [ ] Create user endpoint
  - [ ] Read user(s) endpoint
  - [ ] Update user endpoint
  - [ ] Delete user endpoint
  - [ ] User model with required fields (id, username, email, password, role)

- [ ] **Authentication**
  - [ ] JWT token-based authentication
  - [ ] Login endpoint implementation
  - [ ] Password hashing
  - [ ] Secure token generation and validation

- [ ] **Authorization**
  - [ ] Role-based access control (admin/user roles)
  - [ ] Authorization middleware
  - [ ] Protected route implementation
  - [ ] User-specific access restrictions

- [ ] **API Endpoints**
  - [ ] POST /register
  - [ ] POST /login
  - [ ] GET /users
  - [ ] GET /users/{id}
  - [ ] PUT /users/{id}
  - [ ] DELETE /users/{id}

- [ ] **Docker Setup**
  - [ ] Dockerfile creation
  - [ ] Docker Compose configuration
  - [ ] Database container setup
  - [ ] Environment configuration
  - [ ] Single command deployment

- [ ] **Best Practices Implementation**
  - [ ] Environment configuration (.env)
  - [ ] Dependency injection
  - [ ] Error handling
  - [ ] Input validation
  - [ ] Code documentation
  - [ ] Logging system
  - [ ] Clean code architecture

- [ ] **Documentation**
  - [ ] API documentation (Swagger/ReDoc)
  - [ ] Setup instructions
  - [ ] Architecture explanation
  - [ ] API usage examples
  - [ ] Environment variables documentation

- [ ] **Optional Features**
  - [ ] Unit tests
  - [ ] Integration tests
  - [ ] API rate limiting
  - [ ] CI/CD setup

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

## 📝 API Documentation

### Authentication Endpoints

#### Register User
```http
POST /register
Content-Type: application/json

{
    "username": "example_user",
    "email": "user@example.com",
    "password": "secure_password",
    "role": "user"
}
```

#### Login
```http
POST /login
Content-Type: application/json

{
    "username": "example_user",
    "password": "secure_password"
}
```

### User Management Endpoints

All these endpoints require JWT authentication token in the header:
```http
Authorization: Bearer <your_jwt_token>
```

#### Get All Users (Admin Only)
```http
GET /users
```

#### Get User by ID
```http
GET /users/{user_id}
```

#### Update User (Admin Only)
```http
PUT /users/{user_id}
Content-Type: application/json

{
    "username": "updated_username",
    "email": "updated@example.com",
    "role": "user"
}
```

#### Delete User (Admin Only)
```http
DELETE /users/{user_id}
```

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
