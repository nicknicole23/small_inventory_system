import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { productService, saleService } from '../services/api'
import { Plus, Trash2, ShoppingCart } from 'lucide-react'

export default function CreateSale() {
  const navigate = useNavigate()
  const [products, setProducts] = useState([])
  const [cart, setCart] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    fetchProducts()
  }, [])

  const fetchProducts = async () => {
    try {
      const data = await productService.getAll()
      setProducts(data)
    } catch (err) {
      setError('Failed to load products')
    } finally {
      setLoading(false)
    }
  }

  const addToCart = (product) => {
    const existingItem = cart.find(item => item.product_id === product.id)
    
    if (existingItem) {
      if (existingItem.quantity >= product.stock) {
        alert('Not enough stock!')
        return
      }
      setCart(cart.map(item => 
        item.product_id === product.id 
          ? { ...item, quantity: item.quantity + 1 }
          : item
      ))
    } else {
      setCart([...cart, { 
        product_id: product.id, 
        name: product.name, 
        price: product.price, 
        quantity: 1,
        max_stock: product.stock
      }])
    }
  }

  const removeFromCart = (productId) => {
    setCart(cart.filter(item => item.product_id !== productId))
  }

  const updateQuantity = (productId, newQuantity) => {
    if (newQuantity < 1) return
    const item = cart.find(i => i.product_id === productId)
    if (newQuantity > item.max_stock) {
      alert('Not enough stock!')
      return
    }
    
    setCart(cart.map(item => 
      item.product_id === productId 
        ? { ...item, quantity: newQuantity }
        : item
    ))
  }

  const calculateTotal = () => {
    return cart.reduce((sum, item) => sum + (item.price * item.quantity), 0)
  }

  const handleSubmit = async () => {
    if (cart.length === 0) return
    
    try {
      const saleData = {
        items: cart.map(item => ({
          product_id: item.product_id,
          quantity: item.quantity
        })),
        payment_method: 'cash' // Could add selector for this
      }
      
      await saleService.create(saleData)
      navigate('/sales')
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to create sale')
    }
  }

  const filteredProducts = products.filter(p => 
    p.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    p.sku.toLowerCase().includes(searchTerm.toLowerCase())
  )

  if (loading) return <div className="p-6">Loading...</div>

  return (
    <div className="p-6 h-[calc(100vh-64px)] flex gap-6">
      {/* Product Selection */}
      <div className="flex-1 flex flex-col">
        <div className="mb-4">
          <input
            type="text"
            placeholder="Search products..."
            className="w-full border rounded-lg px-4 py-2"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        
        <div className="grid grid-cols-2 lg:grid-cols-3 gap-4 overflow-y-auto pr-2">
          {filteredProducts.map(product => (
            <button
              key={product.id}
              onClick={() => addToCart(product)}
              disabled={product.stock <= 0}
              className={`p-4 rounded-lg border text-left transition-colors ${
                product.stock <= 0 
                  ? 'bg-gray-100 cursor-not-allowed opacity-60' 
                  : 'bg-white hover:border-blue-500 hover:shadow-sm'
              }`}
            >
              <div className="font-semibold text-gray-800">{product.name}</div>
              <div className="text-sm text-gray-500 mb-2">{product.sku}</div>
              <div className="flex justify-between items-center">
                <span className="font-bold text-blue-600">Ksh {product.price}</span>
                <span className={`text-xs px-2 py-1 rounded ${
                  product.stock > 10 ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                }`}>
                  Stock: {product.stock}
                </span>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Cart / Checkout */}
      <div className="w-96 bg-white rounded-lg shadow-lg flex flex-col">
        <div className="p-4 border-b bg-gray-50 rounded-t-lg">
          <h2 className="text-lg font-bold flex items-center gap-2">
            <ShoppingCart size={20} />
            Current Sale
          </h2>
        </div>

        <div className="flex-1 overflow-y-auto p-4">
          {cart.length === 0 ? (
            <div className="text-center text-gray-500 mt-10">
              Cart is empty
            </div>
          ) : (
            <div className="space-y-4">
              {cart.map(item => (
                <div key={item.product_id} className="flex justify-between items-center">
                  <div className="flex-1">
                    <div className="font-medium">{item.name}</div>
                    <div className="text-sm text-gray-500">Ksh {item.price} x {item.quantity}</div>
                  </div>
                  <div className="flex items-center gap-2">
                    <button 
                      onClick={() => updateQuantity(item.product_id, item.quantity - 1)}
                      className="w-6 h-6 rounded bg-gray-100 flex items-center justify-center hover:bg-gray-200"
                    >
                      -
                    </button>
                    <span className="w-8 text-center">{item.quantity}</span>
                    <button 
                      onClick={() => updateQuantity(item.product_id, item.quantity + 1)}
                      className="w-6 h-6 rounded bg-gray-100 flex items-center justify-center hover:bg-gray-200"
                    >
                      +
                    </button>
                    <button 
                      onClick={() => removeFromCart(item.product_id)}
                      className="text-red-500 hover:text-red-700 ml-2"
                    >
                      <Trash2 size={18} />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="p-4 border-t bg-gray-50 rounded-b-lg">
          <div className="flex justify-between items-center mb-4 text-xl font-bold">
            <span>Total:</span>
            <span>Ksh {calculateTotal().toFixed(2)}</span>
          </div>
          
          {error && (
            <div className="text-red-600 text-sm mb-2">{error}</div>
          )}

          <button
            onClick={handleSubmit}
            disabled={cart.length === 0}
            className={`w-full py-3 rounded-lg font-bold text-white ${
              cart.length === 0
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-700'
            }`}
          >
            Complete Sale
          </button>
        </div>
      </div>
    </div>
  )
}
