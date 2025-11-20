# Django Setup Guide

## Quick Start

### Step 1: Navigate to Django Backend
```bash
cd backend_django
```

### Step 2: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Migrations
```bash
python manage.py migrate
```

This creates all database tables.

### Step 5: Seed Products
```bash
python manage.py seed_products
```

This adds 25 sample products to the database.

### Step 6: Create Admin User (Optional)
```bash
python manage.py createsuperuser
```

Follow prompts to create admin account for Django admin panel.

### Step 7: Start Server
```bash
python manage.py runserver
```

Server runs on: `http://localhost:8000`

## API Endpoints

All endpoints are prefixed with `/api/`

### Test in Browser
- Products: http://localhost:8000/api/products/
- Admin: http://localhost:8000/admin/

## Frontend Changes Needed

Update frontend API URLs from port 5000 to 8000:

### Files to Update:
1. `frontend/src/context/AuthContext.js`
   - Change: `http://localhost:5000` → `http://localhost:8000`

2. `frontend/src/pages/Products.js`
   - Change: `http://localhost:5000` → `http://localhost:8000`

3. `frontend/src/pages/ProductDetail.js`
   - Change: `http://localhost:5000` → `http://localhost:8000`

4. `frontend/src/pages/Cart.js`
   - Change: `http://localhost:5000` → `http://localhost:8000`

5. `frontend/src/pages/Orders.js`
   - Change: `http://localhost:5000` → `http://localhost:8000`

6. `frontend/src/pages/Login.js` and `Register.js`
   - Change: `http://localhost:5000` → `http://localhost:8000`

### Login Endpoint Change
Django uses `/api/login/` instead of `/api/login`

Update `frontend/src/context/AuthContext.js`:
```javascript
// Change from:
await axios.post('http://localhost:5000/api/login', {...})

// To:
await axios.post('http://localhost:8000/api/login/', {...})
// Note: trailing slash and port change
```

## API Differences

### Authentication
- **Flask**: Returns `access_token`
- **Django**: Returns `access` and `refresh` tokens

Update login handler to use `access` instead of `access_token`:
```javascript
const { access, refresh } = response.data;
localStorage.setItem('token', access);
```

### Register Endpoint
- **Flask**: `/api/register`
- **Django**: `/api/register/` (trailing slash)

### Cart Endpoints
- **Flask**: `/api/cart/{id}` for update/delete
- **Django**: `/api/cart/{id}/` (trailing slash)

### Orders Endpoint
- Guest orders: `/api/orders/guest/` (new endpoint)

## Verification

1. **Check Django server is running:**
   ```
   http://localhost:8000/api/products/
   ```
   Should return JSON array of products

2. **Check admin panel:**
   ```
   http://localhost:8000/admin/
   ```
   Login with superuser credentials

3. **Test API:**
   ```bash
   curl http://localhost:8000/api/products/
   ```

## Migration from Flask

| Feature | Flask | Django |
|---------|-------|--------|
| Port | 5000 | 8000 |
| Auth | Flask-JWT-Extended | DRF Simple JWT |
| ORM | SQLAlchemy | Django ORM |
| URL trailing slash | Optional | Required |
| Admin | Custom | Built-in |
| Migrations | Manual | `makemigrations` + `migrate` |

## Next Steps

1. Update frontend API URLs (see above)
2. Test all endpoints
3. Verify authentication works
4. Test guest checkout
5. Check admin panel functionality

Your Django backend is ready! 🚀

