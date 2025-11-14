import { useState, useEffect } from 'react'
import { apiClient } from '../services/api'

function Home() {
  const [serverStatus, setServerStatus] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Test API connection
    const checkServer = async () => {
      try {
        const response = await apiClient.get('/health')
        setServerStatus(response.data)
      } catch (error) {
        console.error('Error connecting to server:', error)
        setServerStatus({ status: 'error', message: 'Cannot connect to server' })
      } finally {
        setLoading(false)
      }
    }

    checkServer()
  }, [])

  return (
    <div className="home">
      <h1>Small Shop Inventory System</h1>
      <p>Welcome to your inventory management system</p>
      
      <div className="server-status">
        <h3>Server Status:</h3>
        {loading ? (
          <p>Checking connection...</p>
        ) : (
          <p style={{ 
            color: serverStatus?.status === 'ok' ? 'green' : 'red' 
          }}>
            {serverStatus?.message || 'Unknown'}
          </p>
        )}
      </div>

      <div className="info-box">
        <h2>Getting Started</h2>
        <ul style={{ textAlign: 'left', maxWidth: '500px', margin: '0 auto' }}>
          <li>Backend API is running on http://localhost:5000</li>
          <li>Frontend is running on http://localhost:5173</li>
          <li>Check the README files for setup instructions</li>
        </ul>
      </div>
    </div>
  )
}

export default Home
