# Quick Start Guide

## Milestone 1: Development Environment Setup - COMPLETED ✅

This guide will help you get your Small Shop Inventory System up and running in minutes.

## 📋 What Was Generated

### Backend (`/backend`)
✅ Flask application with factory pattern  
✅ Configuration for SQLite (dev) and MySQL (prod)  
✅ SQLAlchemy + Flask-Migrate setup  
✅ JWT authentication configuration  
✅ CORS enabled for frontend communication  
✅ Folder structure: `/models`, `/routes`, `/services`  
✅ requirements.txt with all dependencies  
✅ Environment variables template  

### Frontend (`/frontend`)
✅ Vite + React 18 setup  
✅ React Router v6 configuration  
✅ Axios API client with interceptors  
✅ API service layer (auth, products, categories)  
✅ Folder structure: `/components`, `/pages`, `/services`  
✅ Environment configuration for dev/prod  
✅ Home page with server status check  

### Documentation
✅ Comprehensive main README  
✅ Backend-specific README  
✅ Frontend-specific README  
✅ Setup and start scripts  

---

## 🚀 Three Ways to Start

### Option 1: Automated Setup (Recommended)

```bash
# Run the setup script (one time only)
./setup.sh

# Then start both servers
./start.sh
```

### Option 2: Manual Setup

**Terminal 1 - Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

### Option 3: Step-by-Step

See the detailed instructions in the main [README.md](./README.md)

---

## 🎯 Verify Installation

1. **Backend Health Check**  
   Visit: http://localhost:5000/api/health  
   Expected: `{"status": "ok", "message": "Server is running"}`

2. **Frontend**  
   Visit: http://localhost:5173  
   You should see the home page with server status

---

## 📁 Project Structure Overview

```
small_inventory_system/
│
├── 📜 README.md                 # Main documentation
├── 📜 QUICK_START.md           # This file
├── 🔧 setup.sh                 # Automated setup script
├── 🚀 start.sh                 # Start both servers
├── 🙈 .gitignore               # Git ignore rules
│
├── 🐍 backend/                 # Flask REST API
│   ├── app.py                  # Main application (Flask factory)
│   ├── config.py               # Dev/Prod configurations
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example            # Environment template
│   ├── .gitignore              # Backend-specific ignores
│   ├── README.md               # Backend documentation
│   │
│   ├── 📦 models/              # SQLAlchemy models (empty, ready)
│   ├── 🛣️ routes/              # API blueprints (empty, ready)
│   └── ⚙️ services/            # Business logic (empty, ready)
│
└── ⚛️ frontend/                # React + Vite
    ├── index.html              # HTML template
    ├── package.json            # Node dependencies
    ├── vite.config.js          # Vite configuration
    ├── .env.example            # Environment template
    ├── .gitignore              # Frontend-specific ignores
    ├── README.md               # Frontend documentation
    │
    └── src/
        ├── main.jsx            # Entry point
        ├── App.jsx             # Main app with routing
        ├── App.css             # App styles
        ├── index.css           # Global styles
        │
        ├── 📄 pages/           # Route pages
        │   └── Home.jsx        # Home page (with API test)
        │
        ├── 🧩 components/      # Reusable components (empty, ready)
        │
        └── 🔌 services/        # API layer
            └── api.js          # Axios + API services
```

---

## 🔑 Key Files Explained

### Backend

| File | Purpose |
|------|---------|
| `app.py` | Main Flask app with factory pattern, routes, and initialization |
| `config.py` | Configuration classes for dev (SQLite) and prod (MySQL) |
| `requirements.txt` | All Python dependencies (Flask, SQLAlchemy, JWT, etc.) |
| `.env.example` | Template for environment variables |

### Frontend

| File | Purpose |
|------|---------|
| `src/App.jsx` | Main component with React Router setup |
| `src/pages/Home.jsx` | Home page with server status check |
| `src/services/api.js` | Axios client + API service functions |
| `vite.config.js` | Vite config with proxy for API calls |
| `.env.example` | Template for API URL configuration |

---

## 🗄️ Database Quick Reference

### Development (SQLite) - Default
- **Location**: `backend/inventory_dev.db`
- **No setup needed** - created automatically
- **Perfect for**: Development and testing

### Production (MySQL)
- **Setup required**: Create database and user
- **Configuration**: Update `backend/.env`
- **See**: Main README for detailed MySQL setup

**Switch to MySQL:**
```bash
# Edit backend/.env
FLASK_ENV=production
DATABASE_URL=mysql+pymysql://user:pass@localhost/inventory_db
```

---

## 🧪 Test Your Setup

### 1. Backend API Test
```bash
curl http://localhost:5000/api/health
# Expected: {"status":"ok","message":"Server is running"}
```

### 2. Frontend Test
- Open http://localhost:5173
- Check "Server Status" section
- Should show green "Server is running" message

### 3. Database Test
```bash
cd backend
source venv/bin/activate
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); print('Database:', app.config['SQLALCHEMY_DATABASE_URI'])"
```

---

## 📝 Next Steps (Milestone 2)

Now that your environment is set up, you can start building features:

### 1. Create Database Models
- `backend/models/user.py` - User authentication
- `backend/models/product.py` - Product information
- `backend/models/category.py` - Product categories

### 2. Create API Routes
- `backend/routes/auth_routes.py` - Login, register, logout
- `backend/routes/product_routes.py` - CRUD operations
- `backend/routes/category_routes.py` - Category management

### 3. Create Frontend Pages
- `frontend/src/pages/Login.jsx`
- `frontend/src/pages/Dashboard.jsx`
- `frontend/src/pages/Products.jsx`

### 4. Create Components
- `frontend/src/components/Navbar.jsx`
- `frontend/src/components/ProductCard.jsx`
- `frontend/src/components/ProductForm.jsx`

---

## 🛟 Common Issues & Solutions

### ❌ "Port 5000 already in use"
```bash
# Find and kill the process
lsof -i :5000
kill -9 <PID>
```

### ❌ "Module not found" (Backend)
```bash
cd backend
source venv/bin/activate  # Make sure venv is active!
pip install -r requirements.txt
```

### ❌ "Cannot GET /api/..." (Frontend)
- Check if backend is running
- Verify `frontend/.env` has `VITE_API_BASE_URL=http://localhost:5000/api`
- Check CORS settings in `backend/app.py`

### ❌ Database migration errors
```bash
cd backend
rm -rf migrations/ inventory_dev.db
flask db init
flask db migrate -m "Initial"
flask db upgrade
```

---

## 📚 Documentation Links

- **Main README**: [README.md](./README.md) - Complete project overview
- **Backend README**: [backend/README.md](./backend/README.md) - Flask API docs
- **Frontend README**: [frontend/README.md](./frontend/README.md) - React app docs

---

## 🎓 Learning Resources

### Flask
- [Flask Official Docs](https://flask.palletsprojects.com/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)

### React
- [React Official Docs](https://react.dev/)
- [Vite Guide](https://vitejs.dev/guide/)
- [React Router](https://reactrouter.com/)

### API Design
- [REST API Tutorial](https://restfulapi.net/)
- [HTTP Status Codes](https://httpstatuses.com/)

---

## ✅ Milestone 1 Checklist

- [x] Backend folder structure created
- [x] Flask app with factory pattern
- [x] SQLAlchemy + Migrate configured
- [x] JWT authentication setup
- [x] CORS enabled
- [x] Frontend Vite + React setup
- [x] React Router configured
- [x] Axios API client with interceptors
- [x] Environment configuration (dev/prod)
- [x] Comprehensive documentation
- [x] Setup automation scripts

**Status: 🎉 MILESTONE 1 COMPLETE!**

---

## 💡 Tips for Development

1. **Keep backend and frontend terminals separate**
2. **Check API responses in Browser DevTools → Network tab**
3. **Use VS Code extensions**: Python, ESLint, Prettier
4. **Test API endpoints with Postman or Thunder Client**
5. **Commit often with clear messages**
6. **Read the error messages carefully - they usually tell you what's wrong!**

---

**Ready to build something awesome? Let's go! 🚀**
