# 🚀 Deployment Steps - Vercel + Railway

Your app is **ready to deploy**! Follow these steps:

---

## ✅ Pre-Deployment Checklist

- [x] Frontend uses `config.js` for API URLs
- [x] Backend has `requirements.txt` with all dependencies
- [x] Backend has deployment config files (`Procfile`, `railway.json`, `runtime.txt`)
- [x] Frontend has `.env` template
- [x] Database migrations are ready

---

## 🎯 Deployment Steps

### Part 1: Deploy Backend to Railway (15 minutes)

#### Step 1: Sign Up for Railway

1. Go to [railway.app](https://railway.app)
2. Click **"Start a New Project"**
3. Sign in with GitHub

#### Step 2: Create New Project

1. Click **"+ New Project"**
2. Select **"Deploy from GitHub repo"**
3. Connect your GitHub account (if not already connected)
4. Select your repository: `E_commerce_website`
5. Railway will detect it's a Python project

#### Step 3: Configure Backend

1. Railway auto-detects Django, but let's configure it:
   - Click on your deployment
   - Go to **"Settings"**
   - **Root Directory**: `backend_django`
   - **Start Command**: `gunicorn ecommerce_project.wsgi --log-file -`

2. Add PostgreSQL Database:
   - Click **"+ New"** → **"Database"** → **"Add PostgreSQL"**
   - Railway automatically adds `DATABASE_URL` to your environment

#### Step 4: Set Environment Variables

Click **"Variables"** tab and add:

```env
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
DEBUG=False
ALLOWED_HOSTS=.railway.app
CORS_ALLOWED_ORIGINS=https://your-app.vercel.app
GROQ_API_KEY=your-groq-api-key-here
```

**Generate SECRET_KEY:**
```bash
cd backend_django
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

> **Note:** We'll update `CORS_ALLOWED_ORIGINS` after deploying frontend

#### Step 5: Deploy

1. Click **"Deploy"** or push to GitHub (auto-deploys)
2. Wait for build to complete (2-3 minutes)
3. Railway provides your backend URL: `https://your-app.railway.app`

#### Step 6: Run Database Migrations

1. Go to **"Settings"** → **"Deployments"**
2. Click on your deployment → **"View Logs"**
3. Open **"Terminal"** (or use Railway CLI)
4. Run:
   ```bash
   python manage.py migrate
   python manage.py seed_products
   ```

**Or use Railway CLI locally:**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link to your project
railway link

# Run commands
railway run python manage.py migrate
railway run python manage.py seed_products
```

#### Step 7: Test Backend

Open in browser:
```
https://your-app.railway.app/api/products/
```

You should see JSON with products! ✅

---

### Part 2: Deploy Frontend to Vercel (10 minutes)

#### Step 1: Sign Up for Vercel

1. Go to [vercel.com](https://vercel.com)
2. Click **"Sign Up"**
3. Sign in with GitHub

#### Step 2: Import Project

1. Click **"Add New..."** → **"Project"**
2. Import your GitHub repository
3. Vercel detects React app automatically

#### Step 3: Configure Frontend

1. **Framework Preset**: Create React App (auto-detected)
2. **Root Directory**: `frontend`
3. **Build Command**: `npm run build`
4. **Output Directory**: `build`

#### Step 4: Set Environment Variables

Click **"Environment Variables"** and add:

```env
REACT_APP_API_URL=https://your-app.railway.app
```

**Important:** Replace `your-app.railway.app` with your actual Railway URL from Part 1, Step 5.

Example:
```env
REACT_APP_API_URL=https://queens-backend-production.up.railway.app
```

> **Note:** Make sure there's NO trailing slash!

#### Step 5: Deploy

1. Click **"Deploy"**
2. Wait for build (2-3 minutes)
3. Vercel provides your frontend URL: `https://your-app.vercel.app`

#### Step 6: Test Frontend

1. Open: `https://your-app.vercel.app`
2. You should see your homepage! ✅
3. Click **"Products"** - products should load
4. Try adding to cart, chatbot, etc.

---

### Part 3: Connect Frontend to Backend (5 minutes)

#### Step 1: Update Backend CORS

Go back to Railway:

1. Open your backend project
2. Go to **"Variables"**
3. Update `CORS_ALLOWED_ORIGINS`:

```env
CORS_ALLOWED_ORIGINS=https://your-app.vercel.app,https://your-app-git-main.vercel.app
```

**Important:** Use your actual Vercel URL(s). Vercel provides multiple URLs for preview deployments.

Example:
```env
CORS_ALLOWED_ORIGINS=https://queens-store.vercel.app,https://queens-store-git-main.vercel.app
```

4. Railway will automatically redeploy (30 seconds)

#### Step 2: Verify Connection

1. Open your Vercel app: `https://your-app.vercel.app`
2. Open browser DevTools (F12) → **Console** tab
3. Navigate to **Products** page
4. Check console logs - should see:
   ```
   🔄 Fetching products from: https://your-app.railway.app/api/products/
   ✅ API Response received
   ✅ Successfully loaded X products
   ```

5. Check **Network** tab - should see successful requests (Status: 200)

---

## 🎉 Deployment Complete!

Your app is now live:

- **Frontend**: `https://your-app.vercel.app`
- **Backend**: `https://your-app.railway.app`

---

## 🧪 Testing Your Deployed App

### 1. Test Products Page
- [ ] Products load and display
- [ ] Images show correctly
- [ ] Search works
- [ ] Category filter works

### 2. Test Authentication
- [ ] Register new account
- [ ] Login with account
- [ ] Logout

### 3. Test Cart
- [ ] Add product to cart
- [ ] Update quantity
- [ ] Remove from cart
- [ ] See total price in euros (€)

### 4. Test Checkout
- [ ] Checkout as logged-in user
- [ ] Checkout as guest
- [ ] View orders page (logged-in users)

### 5. Test Chatbot
- [ ] Open chatbot
- [ ] Send message
- [ ] Receive AI response (if Groq API key is set)
- [ ] Test multiple questions

---

## 🔧 Troubleshooting

### Frontend can't connect to backend

**Symptom:** Products not loading, network errors

**Solutions:**
1. Check `REACT_APP_API_URL` in Vercel dashboard
2. Make sure Railway backend is running
3. Check Railway logs for errors
4. Verify `CORS_ALLOWED_ORIGINS` includes your Vercel URL

### CORS errors in browser console

**Symptom:**
```
Access to XMLHttpRequest blocked by CORS policy
```

**Solution:**
1. Go to Railway → Variables
2. Update `CORS_ALLOWED_ORIGINS`:
   ```
   https://your-app.vercel.app,https://your-app-git-main.vercel.app
   ```
3. Wait for Railway to redeploy

### Database errors

**Symptom:** 500 errors, "no such table" errors

**Solution:**
```bash
# Use Railway CLI
railway run python manage.py migrate
railway run python manage.py seed_products
```

### Chatbot not responding

**Symptom:** "Oops! Something went wrong"

**Solution:**
1. Check Railway logs for errors
2. Verify `GROQ_API_KEY` is set in Railway
3. Chatbot should fallback to rule-based responses if Groq fails

### Images not loading

**Symptom:** Blank product images

**Solution:**
- Images use Unsplash URLs - check internet connection
- Fallback placeholders should show with product name
- Check browser console for image errors

---

## 🔄 Updating Your Deployment

### Update Frontend

```bash
# Make changes to frontend code
git add .
git commit -m "Update frontend"
git push

# Vercel auto-deploys from GitHub
```

### Update Backend

```bash
# Make changes to backend code
git add .
git commit -m "Update backend"
git push

# Railway auto-deploys from GitHub
```

### Manual Redeploy

**Vercel:**
1. Go to Vercel dashboard
2. Click **"Deployments"**
3. Click **"Redeploy"** on latest deployment

**Railway:**
1. Go to Railway dashboard
2. Click **"Deployments"**
3. Click **"Redeploy"**

---

## 📊 Monitoring

### Railway (Backend)

- View logs: Railway Dashboard → Deployments → View Logs
- Monitor usage: Railway Dashboard → Metrics
- Database: Railway Dashboard → PostgreSQL → Metrics

### Vercel (Frontend)

- View builds: Vercel Dashboard → Deployments
- Monitor traffic: Vercel Dashboard → Analytics
- View logs: Vercel Dashboard → Functions → Logs

---

## 💰 Pricing

### Railway
- **Free Tier**: $5 credit per month
- **Hobby Plan**: $5/month (includes $5 credit)
- Your app should fit in free tier during development

### Vercel
- **Free Tier**: 
  - Unlimited deployments
  - 100GB bandwidth per month
  - Serverless functions
- **Pro Plan**: $20/month (if you need more)

---

## 🎯 Next Steps

### Optional Improvements:

1. **Custom Domain**
   - Vercel: Settings → Domains → Add Domain
   - Railway: Settings → Domains → Add Domain

2. **Environment-based Configuration**
   - Add staging environment
   - Separate production/development databases

3. **CI/CD Pipeline**
   - Add GitHub Actions for tests before deploy
   - Automatic rollback on failed tests

4. **Monitoring & Analytics**
   - Add Sentry for error tracking
   - Add Google Analytics for frontend
   - Add monitoring for backend performance

5. **Performance Optimization**
   - Enable CDN for static assets
   - Add Redis for caching
   - Optimize images

---

## 📚 Helpful Resources

- [Railway Docs](https://docs.railway.app/)
- [Vercel Docs](https://vercel.com/docs)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)

---

## 🆘 Need Help?

If you run into issues:

1. Check Railway logs: `railway logs`
2. Check Vercel logs: Vercel Dashboard → Deployments → View Logs
3. Test backend directly: `https://your-app.railway.app/api/products/`
4. Check browser console for frontend errors
5. Verify all environment variables are set correctly

---

## ✅ Deployment Checklist

### Before Deploying:
- [ ] All code committed to GitHub
- [ ] `requirements.txt` is up to date
- [ ] `package.json` is up to date
- [ ] Environment variables documented

### Railway (Backend):
- [ ] Project created
- [ ] PostgreSQL database added
- [ ] Environment variables set
- [ ] Deployed successfully
- [ ] Database migrations run
- [ ] Products seeded
- [ ] API tested and working

### Vercel (Frontend):
- [ ] Project imported
- [ ] Environment variables set (`REACT_APP_API_URL`)
- [ ] Deployed successfully
- [ ] Site tested and working
- [ ] Products loading
- [ ] Cart working
- [ ] Auth working
- [ ] Chatbot working

### Final:
- [ ] Backend CORS configured with Vercel URL
- [ ] Connection verified (frontend ↔️ backend)
- [ ] All features tested
- [ ] No console errors
- [ ] Images loading
- [ ] Responsive on mobile

---

## 🎊 Congratulations!

Your **👑 The Queens** e-commerce store is now live on the internet! 🚀

Share your links:
- **Frontend**: `https://your-app.vercel.app`
- **Backend API**: `https://your-app.railway.app/api/products/`

Time to celebrate! 🎉

