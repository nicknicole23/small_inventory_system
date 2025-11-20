# Authentication System Setup & Testing Guide

## 📋 What Was Created

### Backend Files

1. **`backend/models/user.py`** - Complete User model with:
   - User fields (username, email, password_hash, first_name, last_name, role, is_active)
   - Password hashing using Werkzeug (set_password, check_password)
   - Helper methods (to_dict, get_full_name, is_admin, is_manager)
   - Marshmallow schemas for validation (Registration, Login, Update)
   - Timestamps (created_at, updated_at)

2. **`backend/routes/auth_routes.py`** - Authentication endpoints:
   - `POST /api/auth/register` - User registration
   - `POST /api/auth/login` - User login (returns JWT tokens)
   - `POST /api/auth/refresh` - Refresh access token
   - `POST /api/auth/logout` - Logout user
   - `GET /api/auth/me` - Get current user info
   - `PUT /api/auth/change-password` - Change password

3. **`backend/test_auth.py`** - Test script for all endpoints

4. **Updated Files**:
   - `backend/models/__init__.py` - Import User model
   - `backend/routes/__init__.py` - Import auth blueprint
   - `backend/app.py` - Register auth blueprint

---

## 🚀 Setup & Run Instructions

### Step 1: Navigate to Backend Directory

```bash
cd /home/munga/Desktop/Nicoles/small_inventory_system/backend
```

### Step 2: Activate Virtual Environment

```bash
source venv/bin/activate
```

### Step 3: Verify Dependencies

The required packages are already in `requirements.txt`:
- Flask
- flask-sqlalchemy
- flask-jwt-extended
- marshmallow
- marshmallow-sqlalchemy
- python-dotenv
- flask-cors

If you haven't installed them yet:

```bash
pip install -r requirements.txt
```

### Step 4: Initialize Database

If you haven't already initialized the database:

```bash
# Initialize migrations (only if not done before)
flask db init

# Create migration for User model
flask db migrate -m "Add User model"

# Apply migration
flask db upgrade
```

### Step 5: Start the Flask Server

```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

---

## 🧪 Testing the Authentication System

### Option 1: Use the Test Script (Automated)

Open a **new terminal** while Flask server is running:

```bash
cd /home/munga/Desktop/Nicoles/small_inventory_system/backend
source venv/bin/activate
python test_auth.py
```

This will automatically test:
1. ✅ User registration
2. ✅ Admin registration
3. ✅ Duplicate registration (should fail)
4. ✅ Valid login
5. ✅ Invalid login (should fail)
6. ✅ Get current user
7. ✅ Refresh token
8. ✅ Change password
9. ✅ Login with new password
10. ✅ Logout

### Option 2: Manual Testing with curl

#### 1. Register a New User

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "first_name": "Test",
    "last_name": "User",
    "role": "staff"
  }'
```

Expected response (201):
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User",
    "role": "staff",
    "is_active": true,
    "created_at": "2025-11-19T...",
    "updated_at": "2025-11-19T..."
  }
}
```

#### 2. Login

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

Expected response (200):
```json
{
  "message": "Login successful",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "testuser",
    ...
  }
}
```

**Save the access_token for next requests!**

#### 3. Get Current User (Protected Route)

```bash
# Replace YOUR_ACCESS_TOKEN with the token from login response
curl -X GET http://localhost:5000/api/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Expected response (200):
```json
{
  "user": {
    "id": 1,
    "username": "testuser",
    ...
  }
}
```

#### 4. Refresh Token

```bash
# Replace YOUR_REFRESH_TOKEN with the refresh token from login
curl -X POST http://localhost:5000/api/auth/refresh \
  -H "Authorization: Bearer YOUR_REFRESH_TOKEN"
```

Expected response (200):
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### 5. Change Password

```bash
curl -X PUT http://localhost:5000/api/auth/change-password \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "current_password": "password123",
    "new_password": "newpassword123"
  }'
```

Expected response (200):
```json
{
  "message": "Password changed successfully"
}
```

#### 6. Logout

```bash
curl -X POST http://localhost:5000/api/auth/logout \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Expected response (200):
```json
{
  "message": "Logout successful. Please remove tokens from client."
}
```

### Option 3: Use Postman or Thunder Client

1. **Install Thunder Client** extension in VS Code
2. **Import the endpoints**:
   - POST `http://localhost:5000/api/auth/register`
   - POST `http://localhost:5000/api/auth/login`
   - GET `http://localhost:5000/api/auth/me` (with Authorization header)
   - POST `http://localhost:5000/api/auth/refresh` (with Authorization header)
   - PUT `http://localhost:5000/api/auth/change-password` (with Authorization header)
   - POST `http://localhost:5000/api/auth/logout` (with Authorization header)

---

## 📝 API Endpoint Details

### 1. Register User
**Endpoint**: `POST /api/auth/register`

**Request Body**:
```json
{
  "username": "string (required, 3-80 chars)",
  "email": "string (required, valid email)",
  "password": "string (required, min 6 chars)",
  "first_name": "string (optional)",
  "last_name": "string (optional)",
  "role": "string (optional: 'admin', 'manager', 'staff', default: 'staff')"
}
```

**Responses**:
- `201`: User created successfully
- `400`: Validation error or user already exists

---

### 2. Login
**Endpoint**: `POST /api/auth/login`

**Request Body**:
```json
{
  "email": "string (required)",
  "password": "string (required)"
}
```

**Responses**:
- `200`: Login successful (returns tokens)
- `401`: Invalid credentials
- `403`: Account inactive

---

### 3. Get Current User
**Endpoint**: `GET /api/auth/me`

**Headers**:
```
Authorization: Bearer <access_token>
```

**Responses**:
- `200`: User information
- `401`: Unauthorized
- `404`: User not found

---

### 4. Refresh Token
**Endpoint**: `POST /api/auth/refresh`

**Headers**:
```
Authorization: Bearer <refresh_token>
```

**Responses**:
- `200`: New access token
- `401`: Invalid refresh token

---

### 5. Change Password
**Endpoint**: `PUT /api/auth/change-password`

**Headers**:
```
Authorization: Bearer <access_token>
```

**Request Body**:
```json
{
  "current_password": "string (required)",
  "new_password": "string (required, min 6 chars)"
}
```

**Responses**:
- `200`: Password changed
- `401`: Invalid current password

---

### 6. Logout
**Endpoint**: `POST /api/auth/logout`

**Headers**:
```
Authorization: Bearer <access_token>
```

**Responses**:
- `200`: Logout successful

---

## 🔐 JWT Token Information

### Token Structure

The JWT tokens contain:

**Claims**:
- `identity`: User ID
- `role`: User role (admin, manager, staff)
- `username`: Username
- `exp`: Expiration time
- `iat`: Issued at time

**Token Expiry**:
- Access Token: 1 hour (configurable in config.py)
- Refresh Token: 30 days (configurable in config.py)

### Using Tokens in Requests

For protected endpoints, include the access token in the Authorization header:

```
Authorization: Bearer <access_token>
```

---

## 🗄️ Database Schema

### Users Table

| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY |
| username | VARCHAR(80) | UNIQUE, NOT NULL, INDEXED |
| email | VARCHAR(120) | UNIQUE, NOT NULL, INDEXED |
| password_hash | VARCHAR(255) | NOT NULL |
| first_name | VARCHAR(50) | NULLABLE |
| last_name | VARCHAR(50) | NULLABLE |
| role | VARCHAR(20) | NOT NULL, DEFAULT 'staff', INDEXED |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE |
| created_at | DATETIME | NOT NULL, DEFAULT NOW |
| updated_at | DATETIME | NOT NULL, DEFAULT NOW, ON UPDATE NOW |

---

## ✅ Verification Checklist

After setup, verify:

- [ ] Flask server starts without errors
- [ ] Database migration completed successfully
- [ ] User registration works (POST /api/auth/register)
- [ ] User login works and returns JWT tokens
- [ ] Protected endpoint (/api/auth/me) requires authentication
- [ ] Invalid credentials return 401 error
- [ ] Duplicate registration returns 400 error
- [ ] Token refresh works
- [ ] Password change works
- [ ] Logout endpoint responds correctly

---

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'werkzeug.security'"

**Solution**: Make sure Flask is installed (it includes werkzeug)
```bash
pip install Flask
```

### Error: "ModuleNotFoundError: No module named 'marshmallow'"

**Solution**: Install marshmallow
```bash
pip install marshmallow marshmallow-sqlalchemy
```

### Error: "flask.cli.NoAppException: Could not locate a Flask application"

**Solution**: Make sure you're in the backend directory and run:
```bash
export FLASK_APP=app.py
```

### Error: Database migration issues

**Solution**: Reset migrations
```bash
rm -rf migrations/
rm inventory_dev.db
flask db init
flask db migrate -m "Add User model"
flask db upgrade
```

### Error: "ImportError: cannot import name 'auth_bp'"

**Solution**: Make sure all files are saved and the import paths are correct

---

## 📚 Next Steps

Now that authentication is complete, you can:

1. **Test all endpoints** using the test script
2. **Create an admin user** for testing
3. **Move to Milestone 2 - Day 2**: JWT middleware and protected routes
4. **Move to frontend**: Create login/register pages

---

## 🎯 User Roles

The system supports three roles:

- **admin**: Full access to all features
- **manager**: Can manage products and inventory
- **staff**: Can view and basic operations

Role-based permissions can be implemented in future endpoints.

---

## 📧 Sample Test Users

Use these for testing:

**Regular User**:
- Email: test@example.com
- Password: password123
- Role: staff

**Admin User**:
- Email: admin@example.com
- Password: admin123
- Role: admin

**Manager User**:
- Email: manager@example.com
- Password: manager123
- Role: manager

---

**Created**: November 19, 2025  
**Status**: ✅ Complete - Ready for Testing

---

**Need help?** Check the main README.md or WORK_PLAN.md for more details!
