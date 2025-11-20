# 📁 Repository Structure - Django Backend

## ✅ Current Active Stack

Your project uses the **Django backend**, not Flask.

```
E_commerce_website/
├── frontend/                  ✅ ACTIVE - React Frontend
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vercel.json           (Deployment config)
│
├── backend_django/           ✅ ACTIVE - Django Backend  ⭐
│   ├── api/                  (Main app)
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── tests.py
│   │   └── management/
│   │       └── commands/
│   │           ├── seed_products.py
│   │           └── update_images.py
│   ├── ecommerce_project/    (Django project)
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── manage.py
│   ├── requirements.txt
│   ├── Procfile             (Railway/Heroku config)
│   ├── railway.json         (Railway config)
│   └── runtime.txt          (Python version)
│
└── backend/                  ⚠️ OLD - Flask Backend (Deprecated)
    ├── app.py               (Not used)
    ├── requirements.txt
    └── reseed_db.py
```

---

## 🎯 What Gets Deployed

### Frontend (Vercel/Netlify):
**Directory:** `frontend/`

**What it contains:**
- React application
- All UI components
- Chatbot frontend
- Authentication context
- API calls (configured to point to Django backend)

**Deployment Configuration:**
- `vercel.json` - Vercel config
- `netlify.toml` - Netlify config
- `package.json` - Dependencies & scripts

---

### Backend (Railway/Render):
**Directory:** `backend_django/` ⭐

**What it contains:**
- Django REST Framework API
- PostgreSQL database models
- JWT authentication
- Groq AI chatbot integration
- 41 unit tests
- Management commands for seeding data

**Deployment Configuration:**
- `Procfile` - Start command: `gunicorn ecommerce_project.wsgi`
- `railway.json` - Railway-specific config
- `runtime.txt` - Python 3.9.18
- `requirements.txt` - All dependencies

---

## 🚀 Deployment Instructions

### Railway (Django Backend)

When deploying to Railway, use these settings:

**1. Root Directory:**
```
backend_django
```

**2. Build Command:**
```bash
pip install -r requirements.txt
```

**3. Start Command:**
```bash
gunicorn ecommerce_project.wsgi --log-file -
```

**4. Environment Variables:**
```env
SECRET_KEY=<generate-random-key>
DEBUG=False
ALLOWED_HOSTS=.railway.app
CORS_ALLOWED_ORIGINS=https://your-vercel-app.vercel.app
DATABASE_URL=<automatically-set-by-railway>
GROQ_API_KEY=<your-groq-api-key>
```

**5. Database:**
- Add PostgreSQL from Railway
- Railway automatically sets `DATABASE_URL`

**6. After Deployment:**
```bash
railway run python manage.py migrate
railway run python manage.py seed_products
```

---

### Vercel (React Frontend)

**1. Root Directory:**
```
frontend
```

**2. Framework Preset:**
```
Create React App
```

**3. Build Command:**
```bash
npm run build
```

**4. Output Directory:**
```
build
```

**5. Environment Variables:**
```env
REACT_APP_API_URL=https://your-railway-backend.railway.app
```

---

## 📊 Why Two Backend Folders?

### `backend/` (Flask - Deprecated)
- Original Flask implementation
- No longer used
- Kept for reference/history

### `backend_django/` (Django - Active) ⭐
- Complete rewrite in Django
- Production-ready
- Better structure
- More features (admin panel, ORM, migrations)
- This is what you should deploy!

---

## 🔄 API Endpoints (Django)

Your Django backend provides these endpoints:

```
Base URL: https://your-app.railway.app

Authentication:
POST   /api/register/        - Create new user
POST   /api/login/           - Get JWT token
POST   /api/token/refresh/   - Refresh JWT token

Products:
GET    /api/products/        - List all products
GET    /api/products/:id/    - Get product details
GET    /api/products/?search=query&category=Electronics

Cart:
GET    /api/cart/            - Get user's cart
POST   /api/cart/            - Add item to cart
PUT    /api/cart/:id/        - Update cart item
DELETE /api/cart/:id/        - Remove from cart

Orders:
GET    /api/orders/          - Get user's orders
POST   /api/orders/          - Create order (authenticated)
POST   /api/orders/guest/    - Create order (guest)

Chatbot:
POST   /api/chatbot/         - Send message to AI chatbot
```

---

## 💡 Quick Verification

### To verify Django backend locally:

```bash
cd backend_django

# Activate virtual environment
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate  # Windows

# Run Django server
python manage.py runserver

# Server starts at: http://localhost:8000
```

### Test endpoints:
```bash
# List products
curl http://localhost:8000/api/products/

# Test chatbot
curl -X POST http://localhost:8000/api/chatbot/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

---

## 📝 Important Notes

### For Deployment:

1. **Use `backend_django/` directory** when deploying backend
2. **NOT `backend/`** - that's the old Flask version
3. Root directory in Railway should be: `backend_django`
4. Start command should be: `gunicorn ecommerce_project.wsgi --log-file -`

### Database:

- **Development:** SQLite (`db.sqlite3`)
- **Production:** PostgreSQL (from Railway)
- Migrations are automatic with `dj-database-url`

### Environment:

- Django automatically switches between SQLite and PostgreSQL
- Based on `DATABASE_URL` environment variable
- If `DATABASE_URL` exists → PostgreSQL
- If not → SQLite (local development)

---

## 🎯 Deployment Checklist

### Railway (Django Backend):
- [ ] Root directory: `backend_django`
- [ ] Add PostgreSQL database
- [ ] Set all environment variables
- [ ] Deploy
- [ ] Run migrations: `railway run python manage.py migrate`
- [ ] Seed products: `railway run python manage.py seed_products`
- [ ] Test API: `https://your-app.railway.app/api/products/`

### Vercel (React Frontend):
- [ ] Root directory: `frontend`
- [ ] Set environment variable: `REACT_APP_API_URL`
- [ ] Deploy
- [ ] Test frontend loads
- [ ] Test products page
- [ ] Test cart functionality
- [ ] Test chatbot

### Connect Them:
- [ ] Update Railway CORS with Vercel URL
- [ ] Verify frontend can fetch products
- [ ] Check browser console for errors
- [ ] Test authentication flow
- [ ] Test checkout process

---

## 🔗 Quick Links

- **Detailed Deployment:** `DEPLOYMENT_STEPS.md`
- **How Connection Works:** `HOW_DEPLOYMENT_WORKS.md`
- **Ready to Deploy:** `READY_TO_DEPLOY.md`

---

**Summary:** Use `backend_django/` for deployment, not `backend/`. The Django backend is your active, production-ready backend! 🚀

