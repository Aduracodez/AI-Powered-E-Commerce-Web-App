# Django E-Commerce Backend

Django REST Framework backend for the e-commerce application.

## Features

- Django REST Framework API
- JWT Authentication (using djangorestframework-simplejwt)
- CORS enabled for frontend communication
- Admin panel for managing products, orders, and users
- Guest checkout support
- SQLite database (can be switched to PostgreSQL/MySQL)

## Installation

### 1. Create Virtual Environment (Recommended)

```bash
cd backend_django
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Migrations

```bash
python manage.py migrate
```

### 4. Create Superuser (Optional - for admin panel)

```bash
python manage.py createsuperuser
```

### 5. Seed Products

```bash
python manage.py seed_products
```

This will add 25 sample products to the database.

### 6. Run Development Server

```bash
python manage.py runserver
```

Server will run on `http://localhost:8000`

## API Endpoints

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
- `PUT /api/cart/{id}/` - Update cart item quantity
- `DELETE /api/cart/{id}/` - Remove from cart

### Orders
- `GET /api/orders/` - Get user's orders (Requires Authentication)
- `POST /api/orders/` - Create order (Requires Authentication)
- `POST /api/orders/guest/` - Create guest order (No auth required)

## Testing API Endpoints

### Register User
```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"testpass123","password2":"testpass123"}'
```

### Login
```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'
```

### Get Products
```bash
curl http://localhost:8000/api/products/
```

### Add to Cart (with token)
```bash
curl -X POST http://localhost:8000/api/cart/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{"product_id":1,"quantity":2}'
```

## Admin Panel

Access Django admin at: `http://localhost:8000/admin/`

Login with superuser credentials to manage:
- Products
- Orders
- Users
- Cart Items

## Project Structure

```
backend_django/
├── manage.py
├── requirements.txt
├── ecommerce_project/
│   ├── settings.py       # Django settings
│   ├── urls.py           # Main URL configuration
│   └── wsgi.py
└── api/
    ├── models.py         # Database models
    ├── serializers.py    # DRF serializers
    ├── views.py          # API views
    ├── urls.py           # API routes
    ├── admin.py          # Admin configuration
    └── management/
        └── commands/
            └── seed_products.py  # Seed command
```

## Frontend Integration

The frontend React app should connect to:
- Base URL: `http://localhost:8000/api/`
- Update `frontend/src/pages/Products.js` and other API calls to use port 8000 instead of 5000

## Database

Default database: SQLite (`db.sqlite3`)

To use PostgreSQL or MySQL, update `DATABASES` in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ecommerce_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Then run migrations again.

## Key Differences from Flask Version

1. **URL Structure**: Django uses `/api/` prefix
   - Flask: `/api/products`
   - Django: `/api/products/` (note trailing slash)

2. **Authentication**: Uses Django REST Framework Simple JWT
   - Token endpoint: `/api/login/` (returns access + refresh tokens)
   - Token in header: `Authorization: Bearer <token>`

3. **Response Format**: DRF automatically formats responses
   - Pagination supported
   - Consistent JSON structure

4. **Admin Panel**: Built-in Django admin for data management

5. **Database**: Uses Django ORM instead of SQLAlchemy
   - Migrations: `python manage.py makemigrations` then `python manage.py migrate`

## Troubleshooting

### Database issues
```bash
# Reset database
rm db.sqlite3
python manage.py migrate
python manage.py seed_products
```

### Port conflicts
If port 8000 is in use:
```bash
python manage.py runserver 8001
```

### CORS issues
Check `CORS_ALLOWED_ORIGINS` in `settings.py` includes your frontend URL.

## License

MIT

