import React, { useState, useEffect, useContext } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { AuthContext } from '../context/AuthContext';
import { API_URL } from '../config';
import './ProductDetail.css';

const ProductDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useContext(AuthContext);
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [quantity, setQuantity] = useState(1);
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetchProduct();
  }, [id]);

  const fetchProduct = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/products/${id}/`);
      setProduct(response.data);
    } catch (error) {
      console.error('Error fetching product:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddToCart = async () => {
    if (user) {
      // Logged in user - use backend cart
      try {
        await axios.post(`${API_URL}/api/cart/`, {
          product_id: parseInt(id),
          quantity: quantity,
        });
        setMessage('Product added to cart!');
        setTimeout(() => setMessage(''), 3000);
      } catch (error) {
        setMessage(error.response?.data?.error || 'Failed to add to cart');
        setTimeout(() => setMessage(''), 3000);
      }
    } else {
      // Guest user - use localStorage
      try {
        const guestCart = JSON.parse(localStorage.getItem('guestCart') || '[]');
        const existingItemIndex = guestCart.findIndex(
          item => item.product_id === parseInt(id)
        );
        
        if (existingItemIndex >= 0) {
          guestCart[existingItemIndex].quantity += quantity;
        } else {
          guestCart.push({
            product_id: parseInt(id),
            quantity: quantity,
            product: {
              id: product.id,
              name: product.name,
              price: product.price,
              image_url: product.image_url,
              stock: product.stock
            }
          });
        }
        
        localStorage.setItem('guestCart', JSON.stringify(guestCart));
        setMessage('Product added to cart!');
        setTimeout(() => setMessage(''), 3000);
      } catch (error) {
        setMessage('Failed to add to cart');
        setTimeout(() => setMessage(''), 3000);
      }
    }
  };

  if (loading) {
    return <div className="loading">Loading product...</div>;
  }

  if (!product) {
    return <div className="no-product">Product not found</div>;
  }

  return (
    <div className="product-detail">
      <div className="container">
        <div className="product-detail-content">
          <div className="product-detail-image">
            <img
              src={product.image_url || 'https://via.placeholder.com/500'}
              alt={product.name}
              loading="lazy"
              onError={(e) => {
                console.warn(`Image failed to load: ${product.image_url}`);
                e.target.onerror = null;
                e.target.src = `https://via.placeholder.com/500?text=${encodeURIComponent(product.name)}`;
              }}
            />
          </div>
          <div className="product-detail-info">
            <h1 className="product-detail-name">{product.name}</h1>
            <p className="product-detail-category">{product.category}</p>
            <p className="product-detail-description">{product.description}</p>
            <div className="product-detail-price">€{product.price.toFixed(2)}</div>
            <div className={`product-detail-stock ${product.stock > 0 ? 'in-stock' : 'out-of-stock'}`}>
              {product.stock > 0 ? `In Stock (${product.stock} available)` : 'Out of Stock'}
            </div>

            {product.stock > 0 && (
              <div className="product-detail-actions">
                <div className="quantity-selector">
                  <label>Quantity:</label>
                  <div className="quantity-controls">
                    <button
                      onClick={() => setQuantity(Math.max(1, quantity - 1))}
                      className="quantity-btn"
                    >
                      -
                    </button>
                    <input
                      type="number"
                      value={quantity}
                      onChange={(e) => {
                        const val = parseInt(e.target.value) || 1;
                        setQuantity(Math.max(1, Math.min(val, product.stock)));
                      }}
                      className="quantity-input"
                      min="1"
                      max={product.stock}
                    />
                    <button
                      onClick={() => setQuantity(Math.min(product.stock, quantity + 1))}
                      className="quantity-btn"
                    >
                      +
                    </button>
                  </div>
                </div>
                <button onClick={handleAddToCart} className="add-to-cart-btn">
                  Add to Cart
                </button>
                {message && <div className="message">{message}</div>}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductDetail;

