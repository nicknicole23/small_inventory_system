# Frontend - Small Shop Inventory System

React + Vite frontend for the inventory management system.

## Tech Stack

- **Framework**: React 18
- **Build Tool**: Vite 5
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **Styling**: CSS (ready for Tailwind/Material-UI)

## Project Structure

```
frontend/
├── src/
│   ├── components/       # Reusable React components
│   ├── pages/           # Page components (routes)
│   ├── services/        # API service layer
│   │   └── api.js      # Axios configuration and API calls
│   ├── App.jsx         # Main App component with routing
│   ├── App.css         # App styles
│   ├── main.jsx        # Application entry point
│   └── index.css       # Global styles
├── public/             # Static assets
├── index.html          # HTML template
├── vite.config.js      # Vite configuration
├── package.json        # Dependencies and scripts
├── .env.example        # Environment variables example
└── .gitignore         # Git ignore rules
```

## Setup Instructions

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment Variables

```bash
cp .env.example .env
# Edit .env file with your API URL
```

### 3. Run Development Server

```bash
npm run dev
```

The app will be available at `http://localhost:5173`

## Available Scripts

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linter
npm run lint
```

## API Configuration

The frontend is configured to communicate with the backend API using Axios.

### Development Mode

In development, the API base URL is configured in `.env`:

```env
VITE_API_BASE_URL=http://localhost:5000/api
```

The Vite proxy is also configured in `vite.config.js` to forward `/api` requests to the backend.

### Production Mode

For production, update the `.env` file:

```env
VITE_API_BASE_URL=https://your-production-api.com/api
```

## Making API Calls

Use the service functions from `src/services/api.js`:

```javascript
import { productService, authService } from './services/api'

// Example: Fetch all products
const products = await productService.getAll()

// Example: Login
const response = await authService.login({
  email: 'user@example.com',
  password: 'password123'
})
```

## Authentication

JWT tokens are automatically handled:

- Access token stored in `localStorage`
- Automatically added to request headers
- Interceptors handle token refresh and errors

## Project Features

### Current
- ✅ Vite + React setup
- ✅ React Router configuration
- ✅ Axios HTTP client with interceptors
- ✅ API service layer (auth, products, categories)
- ✅ Environment configuration
- ✅ Basic home page with server status check

### To Implement
- Authentication pages (Login/Register)
- Product management pages (List/Create/Edit/Delete)
- Category management
- Dashboard
- Inventory tracking
- User profile management

## Component Structure (To Be Created)

```
components/
├── layout/
│   ├── Header.jsx
│   ├── Footer.jsx
│   └── Sidebar.jsx
├── products/
│   ├── ProductList.jsx
│   ├── ProductCard.jsx
│   ├── ProductForm.jsx
│   └── ProductDetail.jsx
├── categories/
│   ├── CategoryList.jsx
│   └── CategoryForm.jsx
└── common/
    ├── Button.jsx
    ├── Input.jsx
    ├── Modal.jsx
    └── Loading.jsx
```

## Pages Structure (To Be Created)

```
pages/
├── Home.jsx              ✅ Created
├── Login.jsx
├── Register.jsx
├── Dashboard.jsx
├── Products.jsx
├── ProductDetail.jsx
├── Categories.jsx
└── NotFound.jsx
```

## Development Tips

1. **Hot Reload**: Vite provides instant hot module replacement
2. **API Testing**: Use browser DevTools Network tab to debug API calls
3. **State Management**: Start with React hooks, add Redux/Zustand if needed
4. **Styling**: Currently using vanilla CSS, can integrate Tailwind or Material-UI

## Building for Production

```bash
# Build the app
npm run build

# The output will be in the `dist` folder
# Deploy the `dist` folder to your hosting service
```

## Troubleshooting

### Cannot connect to backend API

1. Ensure backend is running on `http://localhost:5000`
2. Check CORS settings in backend `app.py`
3. Verify `.env` file has correct `VITE_API_BASE_URL`

### Port 5173 already in use

```bash
# Kill process on port 5173
lsof -i :5173
kill -9 <PID>

# Or specify different port
vite --port 3000
```

### Module not found errors

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```
