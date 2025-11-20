import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { API_URL } from '../config';
import './Products.css';

const Products = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [category, setCategory] = useState('');
  const [search, setSearch] = useState('');

  useEffect(() => {
    fetchProducts();
  }, [category, search]);

  const fetchProducts = async () => {
    try {
      setLoading(true);
      const params = {};
      if (category) params.category = category;
      if (search) params.search = search;
      
      console.log('🔄 Fetching products from:', `${API_URL}/api/products/`);
      console.log('📋 Params:', params);
      
      const response = await axios.get(`${API_URL}/api/products/`, { params });
      
      console.log('✅ API Response received:', {
        status: response.status,
        dataKeys: Object.keys(response.data),
        hasResults: !!response.data.results,
        resultsLength: response.data.results?.length || 0,
        dataLength: Array.isArray(response.data) ? response.data.length : 0
      });
      
      // Handle Django REST Framework pagination format
      const products = response.data.results || (Array.isArray(response.data) ? response.data : []);
      
      console.log('📦 Products processed:', {
        productsReceived: products.length,
        isArray: Array.isArray(products),
        sample: products[0] || null
      });
      
      if (!Array.isArray(products)) {
        console.error('❌ Products is not an array:', typeof products, products);
        setProducts([]);
        return;
      }
      
      setProducts(products);
      
      if (products.length === 0) {
        console.warn('⚠️ No products returned from API. Make sure:');
        console.warn('  1. Backend is running on http://localhost:8000');
        console.warn('  2. Database is seeded (run: python manage.py seed_products)');
        console.warn('  3. Products exist in database');
        console.warn('Full response:', response.data);
      } else {
        console.log(`✅ Successfully loaded ${products.length} products`);
      }
    } catch (error) {
      console.error('❌ Error fetching products:', error);
      console.error('Error details:', {
        message: error.message,
        code: error.code,
        response: error.response?.data,
        status: error.response?.status,
        config: {
          url: error.config?.url,
          method: error.config?.method
        }
      });
      
      if (error.code === 'ECONNREFUSED') {
        console.error('❌ Cannot connect to backend. Make sure backend is running on http://localhost:8000');
      } else if (error.response) {
        console.error('❌ Backend error:', error.response.status, error.response.data);
      } else {
        console.error('❌ Network error:', error.message);
      }
      
      setProducts([]);
    } finally {
      setLoading(false);
    }
  };

  const categories = ['Electronics', 'Fashion', 'Home', 'Accessories', 'Fitness'];

  return (
    <div className="products-page">
      <div className="container">
        <h1 className="page-title">Our Products</h1>

        <div className="filters">
          <div className="search-box">
            <input
              type="text"
              placeholder="Search products..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="search-input"
            />
          </div>
          <div className="category-filters">
            <button
              className={category === '' ? 'filter-btn active' : 'filter-btn'}
              onClick={() => setCategory('')}
            >
              All
            </button>
            {categories.map((cat) => (
              <button
                key={cat}
                className={category === cat ? 'filter-btn active' : 'filter-btn'}
                onClick={() => setCategory(cat)}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>

        {loading ? (
          <div className="loading">Loading products...</div>
        ) : products.length === 0 ? (
          <div className="no-products">No products found</div>
        ) : (
          <div className="products-grid">
            {products.map((product) => (
              <div key={product.id} className="product-card">
                <Link to={`/products/${product.id}`} className="product-link">
                  <div className="product-image">
                    <img 
                      src={product.image_url || 'https://via.placeholder.com/300'} 
                      alt={product.name}
                      loading="lazy"
                      onError={(e) => {
                        console.warn(`Image failed to load: ${product.image_url}`);
                        e.target.onerror = null;
                        e.target.src = `https://via.placeholder.com/300?text=${encodeURIComponent(product.name)}`;
                      }}
                      onLoad={(e) => {
                        // Image loaded successfully
                        if (e.target.src.includes('via.placeholder')) {
                          console.log(`Using placeholder for: ${product.name}`);
                        }
                      }}
                    />
                  </div>
                  <div className="product-info">
                    <h3 className="product-name">{product.name}</h3>
                    <p className="product-description">{product.description}</p>
                    <div className="product-footer">
                      <span className="product-price">€{product.price.toFixed(2)}</span>
                      <span className={`product-stock ${product.stock > 0 ? 'in-stock' : 'out-of-stock'}`}>
                        {product.stock > 0 ? 'In Stock' : 'Out of Stock'}
                      </span>
                    </div>
                  </div>
                </Link>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Products;

