# 🚀 Deploy Django Backend to Railway - Step by Step

## ✅ Your Frontend is Live!
Now let's get your backend deployed and connected.

---

## 🎯 Part 1: Deploy Backend to Railway (15 minutes)

### Step 1: Sign Up for Railway

1. Go to: **https://railway.app**
2. Click **"Login"** or **"Start a New Project"**
3. **Sign in with GitHub** (easiest way)
4. Authorize Railway to access your repositories

---

### Step 2: Create New Project

1. Click **"+ New Project"** (big button)

2. Select **"Deploy from GitHub repo"**

3. **Select your repository:**
   ```
   Aduracodez/AI-Powered-E-Commerce-Web-App
   ```

4. Railway will start deploying automatically

---

### Step 3: Configure Root Directory

Railway might deploy from the project root. We need to tell it to use `backend_django/`:

1. **Click on your deployment** (you'll see it building)

2. **Click "Settings"** tab

3. **Scroll to "Service Settings"**

4. Find **"Root Directory"** or **"Start Command"**

5. **Set these:**
   ```
   Root Directory: backend_django
   Start Command: gunicorn ecommerce_project.wsgi --log-file -
   ```

---

### Step 4: Add PostgreSQL Database

Your Django backend needs a database!

1. In your Railway project, click **"+ New"**

2. Select **"Database"**

3. Select **"Add PostgreSQL"**

4. Railway automatically:
   - Creates the database
   - Adds `DATABASE_URL` environment variable
   - Connects it to your Django service

5. **Done!** Database is ready.

---

### Step 5: Set Environment Variables

**Critical step!** Your Django backend needs these:

1. Click on your **Django service** (not the database)

2. Click **"Variables"** tab

3. Click **"+ Add Variable"** and add each of these:

#### Variable 1: SECRET_KEY
```
Name: SECRET_KEY
Value: <generate a random key - see below>
```

**Generate SECRET_KEY:**
```bash
# Run this in your terminal:
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Copy the output and paste it as the value
```

#### Variable 2: DEBUG
```
Name: DEBUG
Value: False
```

#### Variable 3: ALLOWED_HOSTS
```
Name: ALLOWED_HOSTS
Value: .railway.app
```

#### Variable 4: CORS_ALLOWED_ORIGINS (IMPORTANT!)
```
Name: CORS_ALLOWED_ORIGINS
Value: https://your-vercel-app.vercel.app
```

**Replace with your actual Vercel URL!** For example:
```
https://the-queens-store.vercel.app
```

You can add multiple URLs separated by commas:
```
https://the-queens-store.vercel.app,https://the-queens-store-git-master.vercel.app
```

#### Variable 5: GROQ_API_KEY (Optional - for chatbot)
```
Name: GROQ_API_KEY
Value: <your groq api key from console.groq.com>
```

**Note:** `DATABASE_URL` is already set automatically by Railway!

---

### Step 6: Wait for Deployment

Railway will now:
- ✅ Install Python dependencies
- ✅ Connect to PostgreSQL
- ✅ Deploy your Django app
- ⏱️ Takes about 2-3 minutes

Watch the **"Deployments"** tab for progress.

---

### Step 7: Get Your Backend URL

Once deployed:

1. Go to **"Settings"** tab

2. Scroll to **"Domains"**

3. You'll see something like:
   ```
   https://your-app-name.up.railway.app
   ```

4. **Copy this URL** - you'll need it!

---

### Step 8: Run Database Migrations

Your database exists but has no tables yet. Let's create them:

**Option A: Using Railway Dashboard**

1. Click your Django service
2. Click **"Settings"** → **"Deploy"**
3. Find **"Custom Start Command"** or use the terminal

**Option B: Using Railway CLI (Recommended)**

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Link to your project
railway link

# Run migrations
railway run python manage.py migrate

# Seed products (50 products!)
railway run python manage.py seed_products

# Create admin user (optional)
railway run python manage.py createsuperuser
```

**Option C: Using Railway Web Terminal**

1. Go to your Django service
2. Look for a **"Terminal"** or **"Shell"** option
3. Run:
   ```bash
   python manage.py migrate
   python manage.py seed_products
   ```

---

### Step 9: Test Your Backend

Open in browser:
```
https://your-backend-url.railway.app/api/products/
```

You should see **JSON with 50 products!** 🎉

Example response:
```json
{
  "count": 50,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Wireless Headphones",
      "description": "...",
      "price": "79.99",
      "category": "Electronics",
      "image_url": "..."
    },
    ...
  ]
}
```

If you see this → **Backend is working!** ✅

---

## 🔗 Part 2: Connect Frontend to Backend (5 minutes)

Now let's make your Vercel frontend talk to your Railway backend.

### Step 1: Update Vercel Environment Variable

1. Go to **Vercel Dashboard:** https://vercel.com/dashboard

2. **Click your project** (the-queens-store)

3. **Click "Settings"**

4. **Click "Environment Variables"** (left sidebar)

5. **Add or Update:**
   ```
   Name: REACT_APP_API_URL
   Value: https://your-backend-url.railway.app
   ```

   **Example:**
   ```
   REACT_APP_API_URL = https://queens-backend-production.up.railway.app
   ```

   **⚠️ Important:** NO trailing slash!

6. **Select:** Production, Preview, Development (all three)

7. **Click "Save"**

---

### Step 2: Update Railway CORS

Your backend needs to allow requests from your frontend:

1. Go back to **Railway Dashboard**

2. **Click your Django service**

3. **Click "Variables"**

4. **Find `CORS_ALLOWED_ORIGINS`** (you set this earlier)

5. **Update the value** to your actual Vercel URL:
   ```
   https://the-queens-store.vercel.app,https://the-queens-store-git-master.vercel.app
   ```

   Add all your Vercel URLs (production + preview)

6. **Save**

Railway will automatically redeploy with new settings.

---

### Step 3: Redeploy Frontend

To apply the new environment variable:

1. Go to **Vercel** → **Deployments**

2. Click **three dots (•••)** on latest deployment

3. Click **"Redeploy"**

4. Wait ~1 minute for deployment

---

### Step 4: Test the Connection

1. **Open your Vercel app:**
   ```
   https://your-app.vercel.app
   ```

2. **Click "Products"** in navigation

3. **You should see 50 products!** 🎉

4. **Open browser DevTools** (F12)

5. **Check Console** - should see:
   ```
   ✅ Successfully loaded 50 products
   ```

6. **No CORS errors!**

---

## ✅ Verify Everything Works

### Test These Features:

**1. Products Page**
- [ ] 50 products display
- [ ] Images load
- [ ] Search works
- [ ] Category filter works

**2. Product Details**
- [ ] Click a product
- [ ] See details page
- [ ] "Add to Cart" button works

**3. Authentication**
- [ ] Register new account
- [ ] Login with account
- [ ] Logout

**4. Cart**
- [ ] Add items to cart
- [ ] Update quantity
- [ ] Remove items
- [ ] See total in euros (€)

**5. Checkout**
- [ ] Checkout as logged-in user
- [ ] Checkout as guest
- [ ] Order confirmation

**6. Chatbot**
- [ ] Open chatbot
- [ ] Send message
- [ ] Receive AI response (if Groq API key set)

---

## 🎯 Quick Troubleshooting

### Issue 1: Products Not Loading

**Check:**
- Frontend can reach backend?
- Open: `https://your-backend.railway.app/api/products/`
- Should see JSON

**Fix:**
- Check `REACT_APP_API_URL` in Vercel
- Make sure it's your Railway URL
- Redeploy frontend

---

### Issue 2: CORS Error

**Error in browser:**
```
Access to XMLHttpRequest blocked by CORS policy
```

**Fix:**
1. Go to Railway → Variables
2. Update `CORS_ALLOWED_ORIGINS`
3. Make sure it includes your Vercel URL
4. Railway will redeploy automatically

---

### Issue 3: 500 Error from Backend

**Check Railway logs:**
1. Railway → Click your service
2. Click "Deployments"
3. Click latest deployment
4. Check logs for errors

**Common issues:**
- Missing migrations: `railway run python manage.py migrate`
- No products: `railway run python manage.py seed_products`
- Wrong SECRET_KEY: Check it's set in Variables

---

### Issue 4: Database Error

**Error:** "no such table: api_product"

**Fix:**
```bash
railway run python manage.py migrate
railway run python manage.py seed_products
```

---

## 📊 Your Live URLs

Once everything is deployed:

**Frontend (Vercel):**
```
https://your-app.vercel.app
```

**Backend (Railway):**
```
https://your-backend.railway.app
```

**Backend API Endpoints:**
```
https://your-backend.railway.app/api/products/
https://your-backend.railway.app/api/login/
https://your-backend.railway.app/api/register/
https://your-backend.railway.app/api/cart/
https://your-backend.railway.app/api/orders/
https://your-backend.railway.app/api/chatbot/
```

---

## 🎉 Success Checklist

- [ ] Railway backend deployed
- [ ] PostgreSQL database added
- [ ] Environment variables set
- [ ] Migrations run
- [ ] Products seeded
- [ ] Backend API returns products
- [ ] Vercel environment variable updated
- [ ] Railway CORS configured
- [ ] Frontend redeployed
- [ ] Products load on frontend
- [ ] No CORS errors
- [ ] Cart works
- [ ] Checkout works
- [ ] Chatbot responds

---

## 💰 Pricing

**Railway:**
- **Free tier:** $5 credit/month
- Your app should fit in free tier
- ~$0.20/day if always running

**Vercel:**
- **Free tier:** Unlimited deployments
- 100GB bandwidth/month
- Perfect for this project

**Total:** $0-5/month

---

## 🔄 Auto-Deploy

Both platforms watch your GitHub repo:

```bash
# Make changes
git add .
git commit -m "Add new feature"
git push origin Master

# Automatically:
# ✅ Railway rebuilds backend
# ✅ Vercel rebuilds frontend
# ✅ GitHub Actions runs tests
# 🎉 Live in ~3 minutes
```

---

## 🆘 Need Help?

Tell me:
1. **Railway deployment status** (Success or Error?)
2. **Backend URL** (what's your Railway URL?)
3. **Can you access** `your-railway-url/api/products/`?
4. **Frontend error** (what does browser console show?)
5. **CORS issue?** (any red errors in console?)

I'll help you fix it!

---

## 🎯 Next Steps

After everything works:

1. **Test all features** (use the checklist above)
2. **Share your live app** 🎉
3. **Add to portfolio/resume**
4. **Optional:** Set up custom domain
5. **Optional:** Add more features

---

**Your full-stack AI-powered e-commerce app is about to go live!** 🚀

Follow these steps and let me know when your backend is deployed!

