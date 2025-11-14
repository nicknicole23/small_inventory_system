# Small Shop Inventory System

A full-stack inventory management system built with React and Flask.

## 🚀 Tech Stack

### Frontend
- **React 18** with Vite
- **React Router v6** for routing
- **Axios** for HTTP requests
- **Modern CSS** (ready for styling framework)

### Backend
- **Flask 3.0** REST API
- **SQLAlchemy** ORM
- **Flask-JWT-Extended** for authentication
- **Flask-Migrate** for database migrations
- **Marshmallow** for serialization
- **Flask-CORS** for cross-origin requests

### Database
- **SQLite** for development
- **MySQL** for production

## 📁 Project Structure

```
small_inventory_system/
├── backend/                    # Flask REST API
│   ├── app.py                 # Application factory
│   ├── config.py              # Configuration
│   ├── requirements.txt       # Python dependencies
│   ├── models/                # Database models
│   ├── routes/                # API endpoints
│   ├── services/              # Business logic
│   └── migrations/            # DB migrations
│
├── frontend/                   # React + Vite app
│   ├── src/
│   │   ├── components/        # Reusable components
│   │   ├── pages/            # Page components
│   │   ├── services/         # API client
│   │   ├── App.jsx           # Main app
│   │   └── main.jsx          # Entry point
│   ├── package.json
│   └── vite.config.js
│
└── README.md                   # This file
```

## 🛠️ Installation & Setup

### Prerequisites

- **Python 3.8+**
- **Node.js 18+** and npm
- **Git**
- **MySQL** (for production only)

### Quick Start

#### 1. Clone the Repository

```bash
git clone https://github.com/nicknicole23/small_inventory_system.git
cd small_inventory_system
```

#### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env file if needed

# Initialize database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Run backend server
python app.py
```

Backend will run at: **http://localhost:5000**

#### 3. Frontend Setup

Open a **new terminal** window:

```bash
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env if needed

# Run development server
npm run dev
```

Frontend will run at: **http://localhost:5173**

#### 4. Verify Setup

Open your browser and navigate to:
- Frontend: http://localhost:5173
- Backend API: http://localhost:5000/api/health

You should see a "Server Status: ok" message on the frontend.

## 🗄️ Database Configuration

### Development (SQLite)

SQLite is used by default - **no additional setup required**.

The database file `inventory_dev.db` is created automatically in the backend folder.

### Production (MySQL)

#### 1. Install MySQL

```bash
# Ubuntu/Debian
sudo apt-get install mysql-server

# macOS
brew install mysql

# Start MySQL service
sudo service mysql start  # Linux
brew services start mysql  # macOS
```

#### 2. Create Database

```bash
mysql -u root -p
```

```sql
CREATE DATABASE inventory_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'inventory_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON inventory_db.* TO 'inventory_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

#### 3. Update Backend Configuration

Edit `backend/.env`:

```bash
FLASK_ENV=production
DATABASE_URL=mysql+pymysql://inventory_user:your_secure_password@localhost/inventory_db
SECRET_KEY=your-production-secret-key
JWT_SECRET_KEY=your-production-jwt-secret
```

#### 4. Run Migrations

```bash
cd backend
source venv/bin/activate
flask db upgrade
```

## 🎯 Features (Planned)

### Milestone 1: Development Environment Setup ✅
- [x] Backend Flask setup
- [x] Frontend React setup
- [x] Database configuration
- [x] API client configuration

### Milestone 2: Authentication (Next)
- [ ] User registration
- [ ] User login/logout
- [ ] JWT token management
- [ ] Protected routes

### Milestone 3: Product Management
- [ ] Create products
- [ ] Read products
- [ ] Update products
- [ ] Delete products
- [ ] Product search & filtering

### Milestone 4: Category Management
- [ ] Create categories
- [ ] Manage categories
- [ ] Assign products to categories

### Milestone 5: Inventory Tracking
- [ ] Stock levels
- [ ] Low stock alerts
- [ ] Inventory adjustments
- [ ] Transaction history

### Milestone 6: Reporting & Analytics
- [ ] Sales reports
- [ ] Inventory reports
- [ ] Dashboard with charts

## 📝 API Documentation

### Base URL
- Development: `http://localhost:5000/api`
- Production: `https://your-domain.com/api`

### Endpoints

#### Health Check
```
GET /api/health
```

#### Authentication (To be implemented)
```
POST /api/auth/register    - Register new user
POST /api/auth/login       - Login user
POST /api/auth/refresh     - Refresh access token
POST /api/auth/logout      - Logout user
```

#### Products (To be implemented)
```
GET    /api/products       - Get all products
GET    /api/products/:id   - Get product by ID
POST   /api/products       - Create product
PUT    /api/products/:id   - Update product
DELETE /api/products/:id   - Delete product
```

#### Categories (To be implemented)
```
GET    /api/categories       - Get all categories
GET    /api/categories/:id   - Get category by ID
POST   /api/categories       - Create category
PUT    /api/categories/:id   - Update category
DELETE /api/categories/:id   - Delete category
```

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm run test
```

## 🚀 Deployment

### Backend Deployment

1. **Set environment to production**
2. **Configure MySQL database**
3. **Set secure SECRET_KEY and JWT_SECRET_KEY**
4. **Use production WSGI server** (Gunicorn, uWSGI)
5. **Set up reverse proxy** (Nginx, Apache)

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Frontend Deployment

```bash
cd frontend
npm run build
```

Deploy the `dist` folder to:
- **Vercel**
- **Netlify**
- **AWS S3 + CloudFront**
- **Your own server** (Nginx)

## 📚 Development Workflow

1. **Create a new branch** for your feature
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make changes** in backend or frontend

3. **Test your changes** locally

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Description of changes"
   ```

5. **Push to GitHub**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request** on GitHub

## 🛟 Troubleshooting

### Backend won't start
- Check if virtual environment is activated
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check if port 5000 is available: `lsof -i :5000`

### Frontend won't start
- Delete `node_modules` and reinstall: `rm -rf node_modules && npm install`
- Check if port 5173 is available: `lsof -i :5173`
- Clear npm cache: `npm cache clean --force`

### Cannot connect to API
- Verify backend is running on http://localhost:5000
- Check CORS settings in `backend/app.py`
- Verify `.env` file in frontend has correct `VITE_API_BASE_URL`

### Database errors
- Delete `inventory_dev.db` and migrations folder
- Re-run: `flask db init`, `flask db migrate`, `flask db upgrade`

## 📖 Documentation

- [Backend README](./backend/README.md)
- [Frontend README](./frontend/README.md)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👤 Author

**Nicole**
- GitHub: [@nicknicole23](https://github.com/nicknicole23)

## 🙏 Acknowledgments

- Flask Documentation
- React Documentation
- Vite Documentation

---

**Happy Coding! 🎉**
