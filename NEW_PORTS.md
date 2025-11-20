# New Port Configuration

## ✅ Ports Changed

### Frontend
- **New Port:** 3001 (was 3000)
- **URL:** http://localhost:3001
- **Updated:** `package.json` - Frontend now starts on port 3001

### Backend (Django)
- **New Port:** 8001 (was 8000)
- **URL:** http://localhost:8001
- **Updated:** All frontend API calls now use port 8001

## 🚀 How to Start

### Start Backend (Terminal 1)
```bash
cd backend_django
source venv/bin/activate
python manage.py runserver 8001
```

### Start Frontend (Terminal 2)
```bash
cd frontend
npm start
```

Frontend will automatically start on **port 3001**.

## 🌐 Access Your Store

Open browser: **http://localhost:3001**

## ✅ Files Updated

All frontend API calls updated from port 8000 → 8001:
- ✅ `frontend/src/context/AuthContext.js`
- ✅ `frontend/src/pages/Products.js`
- ✅ `frontend/src/pages/ProductDetail.js`
- ✅ `frontend/src/pages/Cart.js`
- ✅ `frontend/src/pages/Orders.js`
- ✅ `frontend/package.json` - Frontend port changed to 3001
- ✅ `backend_django/ecommerce_project/settings.py` - CORS updated for port 3001

## 🔍 Test API

```bash
curl http://localhost:8001/api/products/
```

Should return JSON with 50 products.

## 📝 Note

The frontend now handles Django REST Framework's pagination format automatically, so products will display correctly even if the API returns paginated results.

