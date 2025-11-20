# ⚡ Quick Deployment Guide

The fastest way to deploy **The Queens** e-commerce store.

## 🎯 5-Minute Deployment

### Step 1: Deploy Backend (Railway)

1. Go to https://railway.app and sign up
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Connect your GitHub account and select your repository
4. Choose **`backend_django`** as root directory
5. Click **"Add variables"** and add:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=*.railway.app
   CORS_ALLOWED_ORIGINS=https://your-frontend-url.vercel.app
   GROQ_API_KEY=your-groq-api-key
   ```
6. Click **"Deploy"**
7. Copy your Railway URL (e.g., `https://your-app.railway.app`)

### Step 2: Deploy Frontend (Vercel)

1. Go to https://vercel.com and sign up
2. Click **"New Project"**
3. Import your GitHub repository
4. Set **Root Directory** to `frontend`
5. Click **"Environment Variables"** and add:
   ```
   REACT_APP_API_URL=https://your-app.railway.app
   ```
6. Click **"Deploy"**
7. Copy your Vercel URL (e.g., `https://your-app.vercel.app`)

### Step 3: Update Backend CORS

1. Go back to Railway dashboard
2. Update **`CORS_ALLOWED_ORIGINS`** variable:
   ```
   CORS_ALLOWED_ORIGINS=https://your-app.vercel.app
   ```
3. Railway will automatically redeploy

---

## ✅ Done!

Your app is now live:
- **Frontend:** https://your-app.vercel.app
- **Backend API:** https://your-app.railway.app/api/products/

---

## 🧪 Test Your Deployment

1. Visit your frontend URL
2. Browse products
3. Register an account
4. Add items to cart
5. Complete a checkout
6. Test the chatbot

---

## 📝 Important Notes

### Generate SECRET_KEY:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Update Requirements (if needed):
Add these to `backend_django/requirements.txt`:
```
gunicorn==21.2.0
psycopg2-binary==2.9.9
whitenoise==6.6.0
dj-database-url==2.1.0
```

### Update Django Settings:
See `DEPLOYMENT_GUIDE.md` for detailed `settings.py` changes needed for production.

---

## 🐛 Troubleshooting

**CORS Errors?**
- Make sure `CORS_ALLOWED_ORIGINS` in Railway includes your Vercel URL

**404 Errors on Frontend Routes?**
- Vercel automatically handles this with `vercel.json` (already created)

**Database Errors?**
- Railway automatically provides PostgreSQL
- Click "+ New" → "Database" → "PostgreSQL" in Railway if not added

**Static Files Not Loading?**
- Run migrations in Railway dashboard console: `python manage.py collectstatic`

---

## 💰 Cost

Both platforms offer generous free tiers:
- **Vercel:** Free (perfect for this app)
- **Railway:** $5/month credit (sufficient for low-medium traffic)

**Total: FREE to start!** 🎉

---

## 🔄 Updates After Deployment

Whenever you update your code:

**Frontend:**
```bash
git push origin main
# Vercel auto-deploys from GitHub
```

**Backend:**
```bash
git push origin main
# Railway auto-deploys from GitHub
```

Both platforms automatically deploy when you push to GitHub!

---

## 📞 Need Help?

Check the full `DEPLOYMENT_GUIDE.md` for:
- Alternative deployment platforms
- Environment variable details
- Production checklist
- Common issues and solutions

