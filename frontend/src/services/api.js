import axios from 'axios'

// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api'

// Create axios instance with default configuration
export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 seconds
})

// Request interceptor - Add auth token to requests
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor - Handle common errors
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response) {
      // Handle specific error codes
      switch (error.response.status) {
        case 401:
          // Unauthorized - clear token and redirect to login
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          // window.location.href = '/login'
          break
        case 403:
          console.error('Access forbidden')
          break
        case 404:
          console.error('Resource not found')
          break
        case 500:
          console.error('Server error')
          break
        default:
          console.error('An error occurred:', error.response.data)
      }
    } else if (error.request) {
      console.error('No response from server')
    } else {
      console.error('Error setting up request:', error.message)
    }
    return Promise.reject(error)
  }
)

// Auth Service
export const authService = {
  login: async (credentials) => {
    const response = await apiClient.post('/auth/login', credentials)
    if (response.data.access_token) {
      localStorage.setItem('access_token', response.data.access_token)
      localStorage.setItem('refresh_token', response.data.refresh_token)
    }
    return response.data
  },

  logout: () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  },

  register: async (userData) => {
    const response = await apiClient.post('/auth/register', userData)
    return response.data
  },

  refreshToken: async () => {
    const refreshToken = localStorage.getItem('refresh_token')
    const response = await apiClient.post('/auth/refresh', {
      refresh_token: refreshToken,
    })
    if (response.data.access_token) {
      localStorage.setItem('access_token', response.data.access_token)
    }
    return response.data
  },
}

// Product Service
export const productService = {
  getAll: async () => {
    const response = await apiClient.get('/products')
    return response.data
  },

  getById: async (id) => {
    const response = await apiClient.get(`/products/${id}`)
    return response.data
  },

  create: async (productData) => {
    const response = await apiClient.post('/products', productData)
    return response.data
  },

  update: async (id, productData) => {
    const response = await apiClient.put(`/products/${id}`, productData)
    return response.data
  },

  delete: async (id) => {
    const response = await apiClient.delete(`/products/${id}`)
    return response.data
  },
}

// Category Service
export const categoryService = {
  getAll: async () => {
    const response = await apiClient.get('/categories')
    return response.data
  },

  getById: async (id) => {
    const response = await apiClient.get(`/categories/${id}`)
    return response.data
  },

  create: async (categoryData) => {
    const response = await apiClient.post('/categories', categoryData)
    return response.data
  },

  update: async (id, categoryData) => {
    const response = await apiClient.put(`/categories/${id}`, categoryData)
    return response.data
  },

  delete: async (id) => {
    const response = await apiClient.delete(`/categories/${id}`)
    return response.data
  },
}

export default apiClient
