# Backend - Small Shop Inventory System

Flask REST API for the inventory management system.

## Tech Stack

- **Framework**: Flask 3.0
- **Database**: SQLite (dev) / MySQL (production)
- **ORM**: SQLAlchemy with Flask-Migrate
- **Authentication**: Flask-JWT-Extended
- **Serialization**: Marshmallow
- **CORS**: Flask-CORS

## Project Structure

```
backend/
├── app.py                 # Main application factory
├── config.py              # Configuration for different environments
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment variables
├── models/               # Database models
├── routes/               # API route blueprints
├── services/             # Business logic layer
└── migrations/           # Database migrations (generated)
```

## Setup Instructions

### 1. Create Virtual Environment

```bash
cd backend
python3 -m venv venv
```

### 2. Activate Virtual Environment

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
cp .env.example .env
# Edit .env file with your configuration
```

### 5. Initialize Database

```bash
# Initialize migrations
flask db init

# Create initial migration
flask db migrate -m "Initial migration"

# Apply migration
flask db upgrade
```

### 6. Run Development Server

```bash
python app.py
```

The API will be available at `http://localhost:5000`

## Database Configuration

### Development (SQLite)

SQLite is used by default for development. No additional configuration needed.

```python
# In .env
FLASK_ENV=development
```

The database file `inventory_dev.db` will be created automatically.

### Production (MySQL)

For production, configure MySQL connection:

1. **Install MySQL** (if not already installed)

2. **Create Database:**
```sql
CREATE DATABASE inventory_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'inventory_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON inventory_db.* TO 'inventory_user'@'localhost';
FLUSH PRIVILEGES;
```

3. **Update .env:**
```bash
FLASK_ENV=production
DATABASE_URL=mysql+pymysql://inventory_user:your_password@localhost/inventory_db
```

4. **Run migrations:**
```bash
flask db upgrade
```

## API Endpoints

### Health Check
- `GET /api/health` - Check if server is running

### Root
- `GET /` - API information

## Development Workflow

1. **Make model changes** in `/models`
2. **Create migration**: `flask db migrate -m "Description"`
3. **Apply migration**: `flask db upgrade`
4. **Rollback if needed**: `flask db downgrade`

## Testing

```bash
# Set testing environment
export FLASK_ENV=testing

# Run tests (to be implemented)
pytest
```

## Common Commands

```bash
# Create new migration
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade

# Rollback last migration
flask db downgrade

# View migration history
flask db history

# Run development server
python app.py

# Run with specific config
FLASK_ENV=production python app.py
```

## Troubleshooting

### Port already in use
```bash
# Find process using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>
```

### Database migration errors
```bash
# Reset migrations
rm -rf migrations/
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### Module import errors
Make sure virtual environment is activated and dependencies are installed.
