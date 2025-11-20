# 🚀 Deployment Guide - The Queens E-Commerce Store

This guide covers multiple deployment options for your Django backend + React frontend application.

## 📋 Table of Contents
1. [Quick Deployment (Recommended)](#quick-deployment)
2. [Frontend Deployment Options](#frontend-deployment)
3. [Backend Deployment Options](#backend-deployment)
4. [Full Stack Deployment](#full-stack-deployment)
5. [Environment Variables](#environment-variables)
6. [Production Checklist](#production-checklist)

---

## 🎯 Quick Deployment (Recommended)

### Option 1: Vercel (Frontend) + Railway (Backend)
**Best for:** Beginners, fastest setup, free tier available

**Time to deploy:** ~15 minutes

---

## 🎨 Frontend Deployment

### A. Deploy to Vercel (Recommended)

**Why Vercel?**
- ✅ Free tier with generous limits
- ✅ Automatic HTTPS
- ✅ Built-in CI/CD
- ✅ Global CDN
- ✅ Zero configuration for React

**Steps:**

1. **Prepare your frontend:**
```bash
cd frontend
npm run build  # Test build locally first
```

2. **Create `vercel.json` in frontend folder:**
```json
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "build"
      }
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/static/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
}
```

3. **Deploy:**
```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
cd frontend
vercel
```

4. **Set environment variables in Vercel dashboard:**
- `REACT_APP_API_URL` = your backend URL

**OR use Vercel Web Interface:**
1. Go to https://vercel.com
2. Click "New Project"
3. Import your GitHub repo
4. Select `frontend` as root directory
5. Add environment variable: `REACT_APP_API_URL`
6. Deploy!

---

### B. Deploy to Netlify

**Steps:**

1. **Create `netlify.toml` in frontend folder:**
```toml
[build]
  command = "npm run build"
  publish = "build"
  
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

2. **Deploy:**
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login and deploy
cd frontend
netlify login
netlify deploy --prod
```

---

### C. Deploy to GitHub Pages

**Steps:**

1. **Install gh-pages:**
```bash
cd frontend
npm install --save-dev gh-pages
```

2. **Add to `package.json`:**
```json
{
  "homepage": "https://yourusername.github.io/E_commerce_website",
  "scripts": {
    "predeploy": "npm run build",
    "deploy": "gh-pages -d build"
  }
}
```

3. **Deploy:**
```bash
npm run deploy
```

---

## 🔧 Backend Deployment

### A. Deploy to Railway (Recommended)

**Why Railway?**
- ✅ $5/month free credit
- ✅ Automatic PostgreSQL database
- ✅ Easy environment variables
- ✅ GitHub integration

**Steps:**

1. **Create `railway.json` in backend_django:**
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python manage.py migrate && gunicorn ecommerce_project.wsgi",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

2. **Update `requirements.txt`:**
```txt
Django==4.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.1
djangorestframework-simplejwt==5.3.0
Pillow==10.1.0
groq==0.9.0
coverage==7.3.4
gunicorn==21.2.0
psycopg2-binary==2.9.9
whitenoise==6.6.0
python-dotenv==1.0.0
```

3. **Update `settings.py` for production:**

Add at the top:
```python
import os
from pathlib import Path
import dj_database_url

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-change-this-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
```

Add database configuration:
```python
# Database
if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
```

Add static files configuration:
```python
# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Whitenoise for serving static files
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

Update CORS:
```python
# CORS settings for production
CORS_ALLOWED_ORIGINS = os.environ.get(
    'CORS_ALLOWED_ORIGINS',
    'http://localhost:3001,http://127.0.0.1:3001'
).split(',')

CORS_ALLOW_CREDENTIALS = True
```

4. **Deploy to Railway:**

**Option A: Using Railway CLI:**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
cd backend_django
railway init

# Deploy
railway up
```

**Option B: Using Railway Dashboard:**
1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Set root directory to `backend_django`
6. Add PostgreSQL database (click "+ New" → "Database" → "PostgreSQL")
7. Set environment variables (see below)
8. Deploy!

**Environment Variables for Railway:**
```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app.railway.app
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
GROQ_API_KEY=your-groq-api-key
DATABASE_URL=postgresql://... (auto-added by Railway)
```

---

### B. Deploy to Render

**Steps:**

1. **Create `render.yaml`:**
```yaml
services:
  - type: web
    name: queens-ecommerce-backend
    env: python
    region: oregon
    buildCommand: "pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate"
    startCommand: "gunicorn ecommerce_project.wsgi:application"
    envVars:
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: False
      - key: DATABASE_URL
        fromDatabase:
          name: queens-db
          property: connectionString

databases:
  - name: queens-db
    region: oregon
    plan: free
```

2. **Deploy:**
- Go to https://render.com
- Click "New +" → "Web Service"
- Connect your GitHub repository
- Render will automatically detect and deploy

---

### C. Deploy to Heroku

**Steps:**

1. **Create `Procfile` in backend_django:**
```
web: gunicorn ecommerce_project.wsgi
release: python manage.py migrate
```

2. **Create `runtime.txt`:**
```
python-3.11.0
```

3. **Deploy:**
```bash
# Install Heroku CLI
# macOS: brew tap heroku/brew && brew install heroku

# Login
heroku login

# Create app
cd backend_django
heroku create queens-ecommerce-backend

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Set environment variables
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=queens-ecommerce-backend.herokuapp.com
heroku config:set CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app

# Deploy
git push heroku main
```

---

## 🌐 Full Stack Deployment

### Option 1: Vercel + Railway (Recommended)

**Frontend (Vercel):**
```bash
cd frontend
vercel --prod
```

**Backend (Railway):**
```bash
cd backend_django
railway up
```

**Connect them:**
1. Get your Railway backend URL: `https://your-app.railway.app`
2. Update frontend environment variable in Vercel:
   - `REACT_APP_API_URL` = `https://your-app.railway.app`
3. Update backend CORS in Railway:
   - `CORS_ALLOWED_ORIGINS` = `https://your-frontend.vercel.app`

---

### Option 2: All-in-One with Render

Deploy both frontend and backend on Render using a monorepo setup.

---

## 🔐 Environment Variables

### Frontend (.env for local, Vercel/Netlify dashboard for production)
```env
REACT_APP_API_URL=https://your-backend.railway.app
```

### Backend (.env for local, Railway/Render dashboard for production)
```env
SECRET_KEY=your-very-long-random-secret-key
DEBUG=False
ALLOWED_HOSTS=your-app.railway.app,your-app.onrender.com
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app,https://your-frontend.netlify.app
DATABASE_URL=postgresql://user:password@host:port/dbname
GROQ_API_KEY=your-groq-api-key
```

**Generate SECRET_KEY:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## ✅ Production Checklist

### Before Deployment:

- [ ] Set `DEBUG=False` in production
- [ ] Update `ALLOWED_HOSTS` with your domain
- [ ] Update `CORS_ALLOWED_ORIGINS` with frontend URL
- [ ] Set strong `SECRET_KEY`
- [ ] Use PostgreSQL (not SQLite) for production
- [ ] Run `python manage.py collectstatic`
- [ ] Test production build locally: `npm run build && serve -s build`
- [ ] Remove any hardcoded API URLs in frontend
- [ ] Add `.env` files to `.gitignore`
- [ ] Set up GROQ_API_KEY if using chatbot

### After Deployment:

- [ ] Test user registration
- [ ] Test login/logout
- [ ] Test product browsing
- [ ] Test add to cart
- [ ] Test checkout (both user and guest)
- [ ] Test chatbot functionality
- [ ] Check API endpoints in browser network tab
- [ ] Verify HTTPS is enabled
- [ ] Test on mobile devices
- [ ] Set up monitoring (Railway/Render dashboards)

---

## 🔧 Update Frontend API URLs

Update all API calls in your frontend to use environment variables:

**src/config.js** (create this file):
```javascript
export const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
```

**Update all files:**
```javascript
// Before:
axios.get('http://localhost:8000/api/products/')

// After:
import { API_URL } from '../config';
axios.get(`${API_URL}/api/products/`)
```

---

## 🐛 Common Issues & Solutions

### Issue 1: CORS Errors
**Solution:** Add frontend URL to `CORS_ALLOWED_ORIGINS` in backend

### Issue 2: 404 on Frontend Routes
**Solution:** Add redirects configuration (see Vercel/Netlify configs above)

### Issue 3: Static Files Not Loading
**Solution:** 
```bash
python manage.py collectstatic --no-input
```

### Issue 4: Database Connection Errors
**Solution:** Check `DATABASE_URL` environment variable is set correctly

### Issue 5: 502 Bad Gateway
**Solution:** Check backend logs, ensure gunicorn is running

---

## 📊 Cost Estimate

### Free Tier Option:
- **Frontend (Vercel):** Free
- **Backend (Railway):** $5/month credit (enough for small app)
- **Database (Railway PostgreSQL):** Included
- **Total:** FREE for low traffic

### Paid Option (More scalability):
- **Frontend (Vercel Pro):** $20/month
- **Backend (Railway Pro):** $20/month
- **Total:** $40/month

---

## 🎓 Recommended Learning Path

1. Start with **Vercel (Frontend)** + **Railway (Backend)**
2. Learn to use environment variables properly
3. Monitor your app's performance
4. Scale up as needed

---

## 📞 Support

If you encounter issues:
1. Check deployment platform logs
2. Check browser console (F12)
3. Verify environment variables are set correctly
4. Test API endpoints directly in browser

---

## 🚀 Quick Start Commands

```bash
# Frontend deployment (Vercel)
cd frontend
vercel --prod

# Backend deployment (Railway)
cd backend_django
railway login
railway up

# Or deploy via web interfaces:
# - Vercel: https://vercel.com
# - Railway: https://railway.app
# - Render: https://render.com
# - Netlify: https://netlify.com
```

---

**Your app is now live! 🎉**

Frontend: `https://your-app.vercel.app`  
Backend API: `https://your-app.railway.app`

