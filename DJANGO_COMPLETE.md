# Django E-Commerce Backend - Complete Setup

## ✅ What's Been Created

A complete Django REST Framework backend that replaces the Flask backend with the same functionality:

### Project Structure
```
backend_django/
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── README.md                    # Detailed documentation
├── ecommerce_project/          # Main Django project
│   ├── settings.py             # Django settings
│   ├── urls.py                 # URL routing
│   ├── wsgi.py                 # WSGI config
│   └── asgi.py                 # ASGI config
└── api/                        # API app
    ├── models.py               # Database models
    ├── serializers.py          # DRF serializers
    ├── views.py                # API views/endpoints
    ├── urls.py                 # API routes
    ├── admin.py                # Admin panel config
    └── management/
        └── commands/
            └── seed_products.py  # Seed command
```

## 🚀 Quick Start

### 1. Setup Django Backend

```bash
cd backend_django

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Seed products
python manage.py seed_products

# Create admin user (optional)
python manage.py createsuperuser

# Start server
python manage.py runserver
```

Server runs on: **http://localhost:8000**

### 2. Update Frontend (Optional)

If you want to use Django backend instead of Flask:

See `FRONTEND_DJANGO_UPDATE.md` for detailed instructions.

**Quick change:**
- Update all API URLs from `http://localhost:5000` to `http://localhost:8000`
- Add trailing slashes to all endpoints (`/api/products/` instead of `/api/products`)

## 📊 Features

### ✅ All Flask Features Implemented

- ✅ User registration and authentication (JWT)
- ✅ Product listing with filters (category, search)
- ✅ Shopping cart (add, update, remove)
- ✅ Order creation (authenticated and guest)
- ✅ Order history
- ✅ Guest checkout support
- ✅ CORS enabled for React frontend

### 🆕 Additional Django Features

- ✅ Django Admin Panel (`/admin/`)
- ✅ Built-in authentication system
- ✅ Database migrations
- ✅ Management commands
- ✅ Better ORM (Django ORM)
- ✅ Automatic API documentation
- ✅ Production-ready structure

## 🔌 API Endpoints

### Authentication
- `POST /api/register/` - Register new user
- `POST /api/login/` - Login (get JWT tokens)
- `POST /api/token/refresh/` - Refresh access token

### Products
- `GET /api/products/` - List all products
- `GET /api/products/?category=Electronics` - Filter by category
- `GET /api/products/?search=laptop` - Search products
- `GET /api/products/{id}/` - Get single product

### Cart (Requires Authentication)
- `GET /api/cart/` - Get user's cart
- `POST /api/cart/` - Add item to cart
- `PUT /api/cart/{id}/` - Update quantity
- `DELETE /api/cart/{id}/` - Remove from cart

### Orders
- `GET /api/orders/` - Get user's orders (Requires Auth)
- `POST /api/orders/` - Create order (Requires Auth)
- `POST /api/orders/guest/` - Create guest order (No auth)

## 🗄️ Database Models

- **Product** - Product catalog
- **CartItem** - Shopping cart items
- **Order** - Customer orders
- **OrderItem** - Items in orders
- **User** - Django's built-in User model

## 🔄 Differences from Flask Version

| Feature | Flask | Django |
|---------|-------|--------|
| Port | 5000 | 8000 |
| Auth Library | Flask-JWT-Extended | DRF Simple JWT |
| ORM | SQLAlchemy | Django ORM |
| Admin Panel | None | Built-in Django Admin |
| Migrations | Manual | `makemigrations` + `migrate` |
| URL Trailing Slash | Optional | Required |
| Token Field Name | `access_token` | `access` (customized to `access_token`) |

## 📝 Key Files Explained

### `api/models.py`
- Defines database models (Product, CartItem, Order, OrderItem)
- Uses Django ORM instead of SQLAlchemy
- Includes field validators and relationships

### `api/serializers.py`
- DRF serializers for API data validation
- Handles request/response formatting
- Custom authentication serializers

### `api/views.py`
- API endpoints using DRF ViewSets
- Product listing with filtering
- Cart management
- Order creation (authenticated + guest)
- Custom authentication views

### `api/urls.py`
- Routes API endpoints
- Uses DRF router for ViewSets
- Custom endpoints for auth and guest orders

### `api/admin.py`
- Configures Django admin panel
- Allows managing products, orders, users via web UI

## 🎯 Next Steps

1. **Test the backend:**
   ```bash
   curl http://localhost:8000/api/products/
   ```

2. **Access admin panel:**
   - Go to: http://localhost:8000/admin/
   - Login with superuser credentials

3. **Update frontend** (if switching to Django):
   - See `FRONTEND_DJANGO_UPDATE.md`
   - Change API URLs to port 8000
   - Add trailing slashes to endpoints

4. **Production deployment:**
   - Update `settings.py` for production
   - Use PostgreSQL instead of SQLite
   - Configure proper CORS origins
   - Use environment variables for secrets

## 🆚 Flask vs Django - Which to Use?

### Use Flask if:
- You want simpler, lightweight backend
- You prefer more control over structure
- Learning Flask specifically
- Port 5000 is already set up

### Use Django if:
- You want built-in admin panel
- You prefer batteries-included framework
- You need migrations and management commands
- You're building for production scale
- You want better ORM and admin features

**Both work the same!** Just different ports (5000 vs 8000).

## 📚 Documentation

- `backend_django/README.md` - Detailed Django setup
- `DJANGO_SETUP.md` - Quick setup guide
- `FRONTEND_DJANGO_UPDATE.md` - Frontend migration guide

## ✨ Summary

You now have **two complete backends**:

1. **Flask** (`backend/`) - Port 5000
2. **Django** (`backend_django/`) - Port 8000

Both provide the same API functionality. Choose based on your preference or switch between them by updating frontend URLs!

🎉 **Django backend is ready to use!**

