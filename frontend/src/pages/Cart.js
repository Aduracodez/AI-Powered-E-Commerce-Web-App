import React, { useState, useEffect, useContext } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import { AuthContext } from '../context/AuthContext';
import { API_URL } from '../config';
import './Cart.css';

const Cart = () => {
  const { user } = useContext(AuthContext);
  const navigate = useNavigate();
  const [cartItems, setCartItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [shippingAddress, setShippingAddress] = useState('');
  const [guestName, setGuestName] = useState('');
  const [guestEmail, setGuestEmail] = useState('');

  useEffect(() => {
    if (user) {
      fetchCart();
    } else {
      fetchGuestCart();
    }
  }, [user]);

  const fetchCart = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/cart/`);
      setCartItems(response.data);
    } catch (error) {
      console.error('Error fetching cart:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchGuestCart = () => {
    try {
      const guestCart = JSON.parse(localStorage.getItem('guestCart') || '[]');
      setCartItems(guestCart);
    } catch (error) {
      console.error('Error fetching guest cart:', error);
    } finally {
      setLoading(false);
    }
  };

  const updateQuantity = async (itemId, newQuantity) => {
    if (newQuantity < 1) return;
    
    if (user) {
      try {
        await axios.put(`${API_URL}/api/cart/${itemId}/`, {
          quantity: newQuantity,
        });
        fetchCart();
      } catch (error) {
        console.error('Error updating cart:', error);
      }
    } else {
      const guestCart = JSON.parse(localStorage.getItem('guestCart') || '[]');
      const itemIndex = guestCart.findIndex(item => item.product_id === itemId);
      if (itemIndex >= 0) {
        guestCart[itemIndex].quantity = newQuantity;
        localStorage.setItem('guestCart', JSON.stringify(guestCart));
        fetchGuestCart();
      }
    }
  };

  const removeItem = async (itemId) => {
    if (user) {
      try {
        await axios.delete(`${API_URL}/api/cart/${itemId}/`);
        fetchCart();
      } catch (error) {
        console.error('Error removing item:', error);
      }
    } else {
      const guestCart = JSON.parse(localStorage.getItem('guestCart') || '[]');
      const filteredCart = guestCart.filter(item => item.product_id !== itemId);
      localStorage.setItem('guestCart', JSON.stringify(filteredCart));
      fetchGuestCart();
    }
  };

  const handleCheckout = async () => {
    if (!shippingAddress.trim()) {
      alert('Please enter a shipping address');
      return;
    }

    if (user) {
      // Authenticated user checkout
      try {
        const response = await axios.post(`${API_URL}/api/orders/`, {
          shipping_address: shippingAddress,
        });
        alert('Order placed successfully!');
        navigate('/orders');
      } catch (error) {
        alert(error.response?.data?.error || 'Failed to place order');
      }
    } else {
      // Guest checkout
      if (!guestName.trim() || !guestEmail.trim()) {
        alert('Please enter your name and email');
        return;
      }

      try {
        const items = cartItems.map(item => ({
          product_id: item.product_id,
          quantity: item.quantity,
          price: item.product.price
        }));

        const response = await axios.post(`${API_URL}/api/orders/guest/`, {
          name: guestName,
          email: guestEmail,
          shipping_address: shippingAddress,
          items: items
        });
        
        localStorage.removeItem('guestCart');
        alert(`Order placed successfully! Order ID: ${response.data.order_id}`);
        navigate('/products');
      } catch (error) {
        alert(error.response?.data?.error || 'Failed to place order');
      }
    }
  };

  const total = cartItems.reduce((sum, item) => {
    const product = item.product || item;
    return sum + product.price * item.quantity;
  }, 0);

  if (loading) {
    return <div className="loading">Loading cart...</div>;
  }

  return (
    <div className="cart-page">
      <div className="container">
        <h1 className="page-title">Shopping Cart</h1>
        {!user && (
          <div style={{ textAlign: 'center', marginBottom: '1rem', color: '#00d4ff', fontSize: '0.9rem' }}>
            Shopping as Guest
          </div>
        )}

        {cartItems.length === 0 ? (
          <div className="empty-cart">
            <p>Your cart is empty</p>
            <Link to="/products" className="shop-link">
              Continue Shopping
            </Link>
          </div>
        ) : (
          <div className="cart-content">
            <div className="cart-items">
              {cartItems.map((item) => {
                const itemId = user ? item.id : item.product_id;
                const product = item.product || item;
                return (
                  <div key={itemId} className="cart-item">
                    <Link to={`/products/${product.id}`} className="cart-item-image">
                      <img
                        src={product.image_url || 'https://via.placeholder.com/150'}
                        alt={product.name}
                        loading="lazy"
                        onError={(e) => {
                          console.warn(`Image failed to load: ${product.image_url}`);
                          e.target.onerror = null;
                          e.target.src = `https://via.placeholder.com/150?text=${encodeURIComponent(product.name)}`;
                        }}
                      />
                    </Link>
                    <div className="cart-item-info">
                      <h3>{product.name}</h3>
                      <p className="cart-item-price">€{product.price.toFixed(2)}</p>
                    </div>
                    <div className="cart-item-quantity">
                      <button
                        onClick={() => updateQuantity(itemId, item.quantity - 1)}
                        className="quantity-btn"
                      >
                        -
                      </button>
                      <span>{item.quantity}</span>
                      <button
                        onClick={() => updateQuantity(itemId, item.quantity + 1)}
                        className="quantity-btn"
                        disabled={item.quantity >= product.stock}
                      >
                        +
                      </button>
                    </div>
                    <div className="cart-item-total">
                      €{(product.price * item.quantity).toFixed(2)}
                    </div>
                    <button
                      onClick={() => removeItem(itemId)}
                      className="remove-btn"
                    >
                      ×
                    </button>
                  </div>
                );
              })}
            </div>

            <div className="cart-summary">
              <h2>Order Summary</h2>
              <div className="summary-row">
                <span>Subtotal:</span>
                <span>€{total.toFixed(2)}</span>
              </div>
              <div className="summary-row">
                <span>Shipping:</span>
                <span>Free</span>
              </div>
              <div className="summary-row total">
                <span>Total:</span>
                <span>€{total.toFixed(2)}</span>
              </div>

              {!user && (
                <>
                  <div className="shipping-address">
                    <label htmlFor="name">Name:</label>
                    <input
                      type="text"
                      id="name"
                      value={guestName}
                      onChange={(e) => setGuestName(e.target.value)}
                      placeholder="Enter your name"
                      style={{
                        width: '100%',
                        padding: '0.75rem',
                        border: '2px solid #2a2a2a',
                        background: '#0f0f0f',
                        color: '#e0e0e0',
                        borderRadius: '5px',
                        fontSize: '1rem',
                        outline: 'none',
                        marginBottom: '1rem'
                      }}
                    />
                  </div>
                  <div className="shipping-address">
                    <label htmlFor="email">Email:</label>
                    <input
                      type="email"
                      id="email"
                      value={guestEmail}
                      onChange={(e) => setGuestEmail(e.target.value)}
                      placeholder="Enter your email"
                      style={{
                        width: '100%',
                        padding: '0.75rem',
                        border: '2px solid #2a2a2a',
                        background: '#0f0f0f',
                        color: '#e0e0e0',
                        borderRadius: '5px',
                        fontSize: '1rem',
                        outline: 'none',
                        marginBottom: '1rem'
                      }}
                    />
                  </div>
                </>
              )}

              <div className="shipping-address">
                <label htmlFor="address">Shipping Address:</label>
                <textarea
                  id="address"
                  value={shippingAddress}
                  onChange={(e) => setShippingAddress(e.target.value)}
                  placeholder="Enter your shipping address"
                  rows="3"
                />
              </div>

              <button onClick={handleCheckout} className="checkout-btn">
                {user ? 'Proceed to Checkout' : 'Place Order as Guest'}
              </button>
              
              {!user && (
                <p style={{ textAlign: 'center', marginTop: '1rem', fontSize: '0.9rem', color: '#b0b0b0' }}>
                  Or <Link to="/register" style={{ color: '#00d4ff' }}>create an account</Link> for order tracking
                </p>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Cart;

