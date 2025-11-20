import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import Home from './pages/Home'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import Inventory from './pages/Inventory'
import Categories from './pages/Categories'
import Sales from './pages/Sales'
import CreateSale from './pages/CreateSale'
import Layout from './components/layout/Layout'
import './App.css'

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          {/* Public Routes */}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          
          {/* Protected Routes (wrapped in Layout) */}
          <Route element={<Layout />}>
            <Route path="/" element={<Home />} />
            <Route path="/inventory" element={<Inventory />} />
            <Route path="/categories" element={<Categories />} />
            <Route path="/sales" element={<Sales />} />
            <Route path="/sales/new" element={<CreateSale />} />
          </Route>

          {/* Redirect unknown routes to login for now */}
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  )
}

export default App
