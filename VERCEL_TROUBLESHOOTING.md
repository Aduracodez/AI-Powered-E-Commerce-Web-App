# 🔧 Vercel Deployment Troubleshooting

## 🎯 Step-by-Step Fix

### Step 1: Check Vercel Build Logs

1. Go to: https://vercel.com/dashboard
2. Click on your project
3. Click on the latest **"Deployment"**
4. Look at the **"Building"** section

**What to look for:**
- ✅ Green checkmark = Build succeeded
- ❌ Red X = Build failed
- Look for error messages in logs

---

## Common Issues & Fixes

### Issue 1: 404 NOT_FOUND Error

**Cause:** Root directory not set to `frontend`

**Fix:**
1. Go to project **Settings**
2. Find **"Root Directory"**
3. Click **"Edit"**
4. Enter: `frontend`
5. Click **"Save"**
6. Go to **"Deployments"** → Click **"Redeploy"**

---

### Issue 2: Build Failed

**Error in logs might say:**
```
npm ERR! code ENOENT
npm ERR! syscall open
npm ERR! path /vercel/path0/package.json
```

**Fix:**
Root directory is wrong. Set to `frontend` (see Issue 1)

---

### Issue 3: "Failed to compile"

**Error might say:**
```
Module not found: Can't resolve 'axios'
```

**Fix - Missing dependencies:**
```bash
cd frontend
npm install
git add package-lock.json
git commit -m "Update package-lock.json"
git push origin Master
```

---

### Issue 4: Environment Variable Missing

**Error might say:**
```
process.env.REACT_APP_API_URL is undefined
```

**Fix:**
1. Go to project **Settings** → **Environment Variables**
2. Add:
   - **Key:** `REACT_APP_API_URL`
   - **Value:** `https://your-railway-backend.railway.app`
3. Click **"Save"**
4. Redeploy

---

## 🚀 Complete Vercel Configuration

### Correct Settings:

```
Project Name: the-queens-store (or any lowercase name)

Root Directory: frontend          ⭐ CRITICAL!

Framework Preset: Create React App

Build Command: npm run build

Output Directory: build

Install Command: npm install
```

### Environment Variables:
```
REACT_APP_API_URL = https://your-backend.railway.app
```

---

## 📝 Quick Diagnostic Commands

Run these locally to verify your frontend works:

```bash
cd /Users/preciousoladapo/Desktop/E_commerce_website/frontend

# Install dependencies
npm install

# Test build (simulates Vercel)
npm run build

# Should create build/ folder
ls -la build/

# Start local server to test build
npx serve -s build -p 3000
```

If local build works but Vercel doesn't, it's a configuration issue.

---

## 🔍 Check These Files

### 1. Verify package.json exists:
```bash
ls frontend/package.json
```

Should show: `frontend/package.json`

### 2. Verify build script:
```bash
cat frontend/package.json | grep "build"
```

Should show: `"build": "react-scripts build"`

### 3. Check for syntax errors:
```bash
cd frontend
npm run build
```

Any errors? Fix them before pushing to Vercel.

---

## 🎯 Most Common Fix (90% of cases)

### The Root Directory Problem:

**Wrong Configuration:**
```
Root Directory: (empty)
```
This makes Vercel look for `package.json` in project root, can't find it → 404

**Correct Configuration:**
```
Root Directory: frontend
```
This makes Vercel look in `frontend/` folder, finds `package.json` → ✅ Works!

---

## 📊 Vercel Dashboard Checklist

Go through these one by one:

### General Settings:
- [ ] Project name is lowercase
- [ ] Root Directory = `frontend`
- [ ] Framework = Create React App

### Build & Development Settings:
- [ ] Build Command = `npm run build`
- [ ] Output Directory = `build`
- [ ] Install Command = `npm install`

### Environment Variables:
- [ ] `REACT_APP_API_URL` is set
- [ ] Value is your Railway backend URL
- [ ] Applied to Production

### Deployments:
- [ ] Latest deployment shows "Ready"
- [ ] Build logs show success
- [ ] No error messages

---

## 🚨 If Still Not Working

### Delete and Recreate:

1. **Delete Project:**
   - Settings → General → Scroll down
   - "Delete Project" → Confirm

2. **Create New Project:**
   - Import from GitHub
   - Select: `Aduracodez/AI-Powered-E-Commerce-Web-App`
   - **Framework:** Create React App
   - **Root Directory:** `frontend` ⭐
   - Add environment variable
   - Deploy

---

## 📱 Test Your Deployment

Once deployed, test these URLs:

```
https://your-app.vercel.app/
→ Should show homepage

https://your-app.vercel.app/products
→ Should show products page

https://your-app.vercel.app/login
→ Should show login page
```

If you get 404 on all pages → Root directory issue
If you get blank page → Check browser console (F12)

---

## 🔍 Debug in Browser

1. Open your Vercel URL
2. Press **F12** (DevTools)
3. Go to **Console** tab
4. Look for errors:

**Common errors:**

❌ `Failed to load resource: 404`
→ Root directory wrong

❌ `CORS policy error`
→ Backend CORS not configured

❌ `Network Error`
→ Backend URL wrong or backend not running

❌ `Unexpected token < in JSON`
→ API returning HTML instead of JSON (404 from backend)

---

## 💡 Pro Tips

### 1. Check Build Locally First:
```bash
cd frontend
npm run build
```
If this fails, Vercel will fail too.

### 2. Use Vercel CLI for Better Debugging:
```bash
npm install -g vercel
cd frontend
vercel
```

### 3. Check Vercel Preview URL:
Every deployment gets a unique URL. Test that first before worrying about the production URL.

---

## 📞 What to Tell Me

If still not working, tell me:

1. **Error message** (from Vercel build logs)
2. **What you see** (404, blank page, error page)
3. **Browser console errors** (F12 → Console)
4. **Vercel build status** (Success or Failed)
5. **Root Directory setting** (What is it currently?)

I'll help you fix it!

---

## ✅ Expected Result

When working, you should see:

**Vercel Deployment:**
- Status: ✅ Ready
- Build: ✅ Completed
- Runtime: ✅ Deployed

**Your Site:**
- Homepage loads
- Products page works
- Navigation works
- (Products won't load until backend is connected)

**Browser Console:**
- No 404 errors
- Might see CORS errors (normal until backend connected)
- No build errors

---

## 🎯 Next Steps

1. Check your Root Directory setting
2. Make sure it says: `frontend`
3. Redeploy
4. Let me know what errors you see!

