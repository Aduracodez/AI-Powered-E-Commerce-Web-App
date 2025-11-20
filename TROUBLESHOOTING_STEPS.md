# 🔧 Troubleshooting Guide - Backend Issues

## ✅ What I've Verified

1. ✅ **Backend server is running** on port 8000
2. ✅ **Products API is working** - Returns 50 products
3. ✅ **Chatbot API is working** - Returns responses
4. ✅ **Groq package is installed**
5. ✅ **Frontend is running** on port 3001
6. ✅ **All API endpoints are correct** - Using port 8000

## 🚨 Most Likely Issue: Backend Server Needs Restart

The backend server was running **before** we installed the Groq package. It needs to be restarted to pick up the new package.

## 🔄 Step-by-Step Fix

### Step 1: Stop the Current Backend Server

**Find and stop the running server:**

```bash
# Find the process
lsof -i :8000

# Kill it (replace PID with the number from above)
kill -9 <PID>
```

**Or simply press `Ctrl+C` in the terminal where the backend is running**

### Step 2: Restart Backend Server

```bash
cd backend_django
source venv/bin/activate
python manage.py runserver 8000
```

**You should see:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### Step 3: Verify Everything Works

**Test Products:**
```bash
curl http://localhost:8000/api/products/ | python3 -m json.tool | head -20
```
Should show products.

**Test Chatbot:**
```bash
curl -X POST http://localhost:8000/api/chatbot/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```
Should return a response.

### Step 4: Refresh Frontend

1. **Hard refresh browser:** `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows)
2. **Open browser console:** F12 or Cmd+Option+I
3. **Check for errors** in the Console tab

## 🔍 Detailed Debugging

### Check Backend Logs

Look at your backend server terminal. You should see requests coming in:
```
[19/Nov/2025 ...] "GET /api/products/ HTTP/1.1" 200 ...
[19/Nov/2025 ...] "POST /api/chatbot/ HTTP/1.1" 200 ...
```

If you see errors, share them with me.

### Check Browser Console

1. Open your browser: http://localhost:3001
2. Press `F12` (or `Cmd+Option+I` on Mac)
3. Go to **Console** tab
4. Look for red error messages
5. Go to **Network** tab
6. Refresh the page
7. Look for failed requests (they'll be in red)

### Common Issues

#### ❌ "Network Error" or "Connection Refused"
- **Cause:** Backend server not running
- **Fix:** Restart backend server (see Step 1-2 above)

#### ❌ "CORS Error"
- **Cause:** Backend CORS settings
- **Fix:** Check `backend_django/ecommerce_project/settings.py` has:
  ```python
  CORS_ALLOWED_ORIGINS = [
      "http://localhost:3001",
      "http://127.0.0.1:3001",
  ]
  ```

#### ❌ "Cannot GET /api/products/"
- **Cause:** Backend not running or wrong port
- **Fix:** Verify backend is running on port 8000

#### ❌ Products Show But Chatbot Doesn't Work
- **Cause:** Groq package issue or API key issue
- **Fix:** Chatbot falls back to rule-based system automatically
- **Note:** This is OK! Rule-based system works fine without API key

#### ❌ Blank Page / No Products
- **Cause:** Frontend can't connect to backend
- **Fix:** 
  1. Check backend is running
  2. Check browser console for errors
  3. Verify frontend API calls use `http://localhost:8000`

## 📋 Quick Diagnostic Commands

Run these to check everything:

```bash
# 1. Check if backend is running
lsof -i :8000

# 2. Test products API
curl http://localhost:8000/api/products/ | python3 -c "import sys, json; data=json.load(sys.stdin); print(f'✅ {len(data.get(\"results\", data))} products')"

# 3. Test chatbot API
curl -X POST http://localhost:8000/api/chatbot/ -H "Content-Type: application/json" -d '{"message": "test"}' | python3 -m json.tool

# 4. Check if frontend is running
lsof -i :3001

# 5. Verify Groq is installed
cd backend_django && source venv/bin/activate && python -c "from groq import Groq; print('✅ Groq installed')"
```

## 🆘 Still Not Working?

Share with me:
1. **What error message** you see (if any)
2. **Browser console errors** (F12 → Console tab)
3. **Backend server output** (what shows in terminal)
4. **What specifically isn't working:**
   - Products not showing?
   - Chatbot not responding?
   - Both?

I can help fix the specific issue!

## ✅ Expected Result After Fix

- **Products page:** http://localhost:3001/products should show 50 products
- **Chatbot:** Click 💬 button → Type message → Should get response
- **No errors** in browser console
- **Backend logs** show successful requests

