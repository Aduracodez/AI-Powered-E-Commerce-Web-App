# Frontend Update for Django Backend

To use the Django backend instead of Flask, update the following files:

## Files to Update

### 1. `frontend/src/context/AuthContext.js`

Change port from 5000 to 8000 and add trailing slashes:

```javascript
// Line 22: Change login endpoint
const response = await axios.post('http://localhost:8000/api/login/', {
  username,
  password,
});

// Line 42: Change register endpoint  
const response = await axios.post('http://localhost:8000/api/register/', {
  username,
  email,
  password,
});
```

### 2. `frontend/src/pages/Products.js`

```javascript
// Line 23: Update API URL
const response = await axios.get('http://localhost:8000/api/products/', { params });
```

### 3. `frontend/src/pages/ProductDetail.js`

```javascript
// Line 22: Update API URL
const response = await axios.get(`http://localhost:8000/api/products/${id}/`);

// Line 35: Update cart endpoint
await axios.post('http://localhost:8000/api/cart/', {
  product_id: parseInt(id),
  quantity: quantity,
});
```

### 4. `frontend/src/pages/Cart.js`

```javascript
// Line 26: Update cart GET
const response = await axios.get('http://localhost:8000/api/cart/');

// Line 51: Update cart PUT
await axios.put(`http://localhost:8000/api/cart/${itemId}/`, {
  quantity: newQuantity,
});

// Line 72: Update cart DELETE
await axios.delete(`http://localhost:8000/api/cart/${itemId}/`);

// Line 94: Update orders POST (authenticated)
const response = await axios.post('http://localhost:8000/api/orders/', {
  shipping_address: shippingAddress,
});

// Line 116: Update guest order POST
const response = await axios.post('http://localhost:8000/api/orders/guest/', {
  name: guestName,
  email: guestEmail,
  shipping_address: shippingAddress,
  items: items
});
```

### 5. `frontend/src/pages/Orders.js`

```javascript
// Update orders GET
const response = await axios.get('http://localhost:8000/api/orders/');
```

## Quick Find & Replace

You can use find & replace in your editor:

1. Find: `http://localhost:5000/api`
2. Replace: `http://localhost:8000/api`
3. Then add trailing slashes to endpoints:
   - Find: `api/login` → Replace: `api/login/`
   - Find: `api/register` → Replace: `api/register/`
   - Find: `api/products` → Replace: `api/products/`
   - Find: `api/cart` → Replace: `api/cart/`
   - Find: `api/orders` → Replace: `api/orders/`

**Note:** Trailing slashes are required in Django URLs.

## Testing After Update

1. Start Django backend: `cd backend_django && python manage.py runserver`
2. Start frontend: `cd frontend && npm start`
3. Test:
   - Login/Register
   - View products
   - Add to cart
   - Checkout (both logged in and guest)

## Keep Both Backends

You can keep both Flask and Django backends:
- Flask: `backend/` (port 5000)
- Django: `backend_django/` (port 8000)

Just update frontend to use the one you want!

