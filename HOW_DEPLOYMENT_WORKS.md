# 🔗 How Vercel Frontend Connects to Railway Backend

## 📊 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         USER'S BROWSER                       │
│                                                              │
│  https://your-app.vercel.app                                │
│  ┌────────────────────────────────────────────────┐        │
│  │  React App (Static HTML, CSS, JS)              │        │
│  │  - Components                                   │        │
│  │  - Routing                                      │        │
│  │  - UI Logic                                     │        │
│  └────────────────────────────────────────────────┘        │
│                         │                                    │
│                         │ axios.get/post                     │
│                         ▼                                    │
└─────────────────────────────────────────────────────────────┘
                          │
                          │ HTTP Requests
                          │ (over internet)
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                  https://your-app.railway.app               │
│  ┌────────────────────────────────────────────────┐        │
│  │  Django Backend (Server Running)               │        │
│  │  - API Endpoints                                │        │
│  │  - Database (PostgreSQL)                        │        │
│  │  - Authentication                               │        │
│  │  - Business Logic                               │        │
│  └────────────────────────────────────────────────┘        │
│                  RAILWAY SERVER                              │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 How They Connect

### 1. **Environment Variables** (The Connection Bridge)

**Frontend (Vercel) knows Backend URL via environment variable:**

```javascript
// frontend/src/config.js
export const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// When deployed to Vercel:
// REACT_APP_API_URL = 'https://your-app.railway.app'
```

**Example API Call:**
```javascript
// frontend/src/pages/Products.js
import { API_URL } from '../config';

const fetchProducts = async () => {
  // This becomes: https://your-app.railway.app/api/products/
  const response = await axios.get(`${API_URL}/api/products/`);
  setProducts(response.data);
};
```

### 2. **CORS Configuration** (Permission to Connect)

**Backend (Railway) allows Frontend URL via CORS:**

```python
# backend_django/ecommerce_project/settings.py
CORS_ALLOWED_ORIGINS = [
    'https://your-app.vercel.app',  # Your Vercel frontend URL
]

# This tells the backend:
# "Allow requests from your-app.vercel.app"
```

**Without CORS, browser blocks the connection:**
```
❌ Access to XMLHttpRequest at 'https://your-app.railway.app/api/products/' 
   from origin 'https://your-app.vercel.app' has been blocked by CORS policy
```

**With CORS configured:**
```
✅ Request allowed - data flows freely
```

---

## 🎯 Step-by-Step Connection Flow

### Example: User Loads Product Page

**1. User visits:** `https://your-app.vercel.app/products`

**2. Browser downloads React app from Vercel:**
- HTML file
- JavaScript bundles
- CSS files
- All static assets

**3. React app runs in browser:**
```javascript
// Products.js component mounts
useEffect(() => {
  fetchProducts(); // This function runs
}, []);
```

**4. Frontend makes HTTP request to backend:**
```javascript
const response = await axios.get(
  'https://your-app.railway.app/api/products/'
);
```

**5. Request travels over internet to Railway:**
```
Browser → Internet → Railway Server → Django → Database
```

**6. Django processes request:**
```python
# backend_django/api/views.py
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()  # Get products from database
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
```

**7. Railway sends response back:**
```
Database → Django → Railway Server → Internet → Browser
```

**8. Frontend displays data:**
```javascript
setProducts(response.data); // Update React state
// Products appear on screen
```

---

## 🔧 Configuration Example

### Complete Setup:

**Step 1: Deploy Backend to Railway**

Environment Variables:
```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-app.railway.app
CORS_ALLOWED_ORIGINS=https://your-app.vercel.app
DATABASE_URL=postgresql://... (auto-provided by Railway)
```

Railway URL: `https://your-app.railway.app`

**Step 2: Deploy Frontend to Vercel**

Environment Variables:
```env
REACT_APP_API_URL=https://your-app.railway.app
```

Vercel URL: `https://your-app.vercel.app`

**Step 3: Update Backend CORS**

Go back to Railway and update:
```env
CORS_ALLOWED_ORIGINS=https://your-app.vercel.app
```

Railway automatically redeploys with new settings.

---

## 💡 Real Example with All API Calls

```javascript
// frontend/src/config.js
export const API_URL = 'https://queens-backend.railway.app';

// frontend/src/pages/Products.js
import { API_URL } from '../config';

// Fetch products
axios.get(`${API_URL}/api/products/`)
// Actual request: https://queens-backend.railway.app/api/products/

// Login
axios.post(`${API_URL}/api/login/`, { username, password })
// Actual request: https://queens-backend.railway.app/api/login/

// Add to cart
axios.post(`${API_URL}/api/cart/`, { product_id, quantity })
// Actual request: https://queens-backend.railway.app/api/cart/
```

---

## 🔐 Security Flow

### 1. **Authentication Example:**

```javascript
// User logs in on frontend
const response = await axios.post(
  'https://your-app.railway.app/api/login/',
  { username: 'user', password: 'pass' }
);

// Backend returns JWT token
const token = response.data.access_token;

// Frontend stores token
localStorage.setItem('token', token);

// Future requests include token
axios.get(`${API_URL}/api/orders/`, {
  headers: { Authorization: `Bearer ${token}` }
});
```

### 2. **CORS Headers in Action:**

**Browser sends request with Origin header:**
```http
GET /api/products/ HTTP/1.1
Host: your-app.railway.app
Origin: https://your-app.vercel.app
```

**Backend checks CORS and responds:**
```http
HTTP/1.1 200 OK
Access-Control-Allow-Origin: https://your-app.vercel.app
Access-Control-Allow-Credentials: true
Content-Type: application/json

{"results": [...products...]}
```

---

## 🎨 What Gets Deployed Where

### Vercel (Frontend):
```
your-app.vercel.app/
├── index.html
├── static/
│   ├── js/
│   │   └── main.abc123.js  (React app bundled)
│   ├── css/
│   │   └── main.def456.css
│   └── media/
│       └── images...
```

**Contains:**
- ✅ HTML, CSS, JavaScript files
- ✅ React components (compiled to JS)
- ✅ Images and assets
- ❌ NO server
- ❌ NO database
- ❌ NO Python/Django code

### Railway (Backend):
```
your-app.railway.app/
├── Django Server (running with Gunicorn)
├── PostgreSQL Database
├── API Endpoints
│   ├── /api/products/
│   ├── /api/login/
│   ├── /api/cart/
│   └── /api/orders/
```

**Contains:**
- ✅ Django server (always running)
- ✅ PostgreSQL database
- ✅ All Python backend code
- ✅ API endpoints
- ❌ NO frontend files
- ❌ NO React code

---

## 🔍 How to Test the Connection

### 1. **Test Backend Directly:**

Open in browser:
```
https://your-app.railway.app/api/products/
```

Should see JSON response:
```json
{
  "results": [
    {
      "id": 1,
      "name": "Product Name",
      "price": "99.99",
      ...
    }
  ]
}
```

### 2. **Test Frontend Connection:**

Open browser DevTools (F12) → Network tab

Visit: `https://your-app.vercel.app/products`

You'll see requests to:
```
https://your-app.railway.app/api/products/
Status: 200 OK
```

### 3. **Check for CORS Issues:**

If you see:
```
CORS policy: No 'Access-Control-Allow-Origin' header
```

**Fix:** Update `CORS_ALLOWED_ORIGINS` in Railway to include your Vercel URL.

---

## 🛠️ Common Connection Issues

### Issue 1: Frontend can't reach backend

**Symptom:**
```
Network Error
ERR_NAME_NOT_RESOLVED
```

**Solution:**
- Check `REACT_APP_API_URL` is correct in Vercel
- Make sure Railway app is running (check Railway dashboard)

### Issue 2: CORS errors

**Symptom:**
```
Access blocked by CORS policy
```

**Solution:**
```python
# backend_django/ecommerce_project/settings.py
CORS_ALLOWED_ORIGINS = [
    'https://your-app.vercel.app',  # Add your Vercel URL
]
```

### Issue 3: 404 errors on API calls

**Symptom:**
```
GET https://your-app.railway.app/api/products/ 404
```

**Solution:**
- Check URL in `config.js` doesn't have double slashes
- Verify Railway backend is deployed and migrations are run

---

## 📝 Update Checklist

When you deploy, update these:

### ✅ Railway Dashboard:
1. `ALLOWED_HOSTS` = your Railway URL
2. `CORS_ALLOWED_ORIGINS` = your Vercel URL
3. `SECRET_KEY` = generated secret
4. `DEBUG` = False

### ✅ Vercel Dashboard:
1. `REACT_APP_API_URL` = your Railway URL

### ✅ Code (if needed):
```javascript
// frontend/src/config.js
export const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
```

---

## 🎯 Summary

**The connection is simple:**

1. **Vercel** hosts your React app as static files
2. **User's browser** downloads and runs React app
3. **React app** makes HTTP requests to Railway backend URL
4. **Railway** receives requests, processes them, returns data
5. **CORS** allows this cross-origin communication
6. **Environment variables** tell frontend where backend lives

**Key Point:** The frontend and backend are completely separate applications that communicate via HTTP over the internet, just like any other API!

---

## 🔗 Visual Connection Summary

```
User Browser
    ↓ [visits]
Vercel (Frontend)
    ↓ [downloads React app]
Browser (React running)
    ↓ [makes HTTP requests]
Railway (Backend API)
    ↓ [queries]
Database (PostgreSQL)
    ↓ [returns data]
Railway
    ↓ [sends JSON]
Browser
    ↓ [displays]
User sees products! 🎉
```

**They connect through:** Environment variables + CORS + HTTP requests

