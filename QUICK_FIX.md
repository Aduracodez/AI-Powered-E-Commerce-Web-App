# Quick Fix: Products Not Showing

## Most Common Issue: Backend Not Running

### Step 1: Install Backend Dependencies (if not done)
```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Start Backend Server
```bash
cd backend
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Restarting with stat
```

**IMPORTANT:** Leave this terminal running! The backend must stay running.

### Step 3: Start Frontend (in a NEW terminal)
```bash
cd frontend
npm start
```

### Step 4: Test in Browser
1. Open: http://localhost:3000
2. Click "Products" in navigation
3. You should see products

---

## Quick Test - Is Backend Working?

Open this URL in your browser:
```
http://localhost:5000/api/products
```

**Expected:** JSON array with products like:
```json
[
  {
    "id": 1,
    "name": "Wireless Headphones",
    "price": 199.99,
    ...
  },
  ...
]
```

**If you see an error:**
- Backend is not running → Start it with `python app.py`
- Connection refused → Backend is not on port 5000
- Empty array `[]` → Database needs to be seeded (restart backend)

---

## Verify Database Has Products

### Method 1: Check Backend Logs
When you start the backend, it should automatically:
1. Create database if it doesn't exist
2. Seed products if database is empty

Look for no errors in the backend terminal.

### Method 2: Delete and Recreate Database
```bash
cd backend
rm -f ecommerce.db
python app.py
```

This will recreate the database with all 20 products.

---

## Check Browser Console

1. Open your frontend: http://localhost:3000
2. Press F12 (open DevTools)
3. Go to Console tab
4. Navigate to Products page
5. Look for error messages:

**Common Errors:**
- `ECONNREFUSED` → Backend not running
- `CORS error` → Backend CORS not configured (should be fine)
- `404` → Wrong API URL
- `Network Error` → Backend not accessible

---

## Still Not Working?

1. **Check both servers are running:**
   - Backend on port 5000 ✓
   - Frontend on port 3000 ✓

2. **Test API directly:**
   ```bash
   curl http://localhost:5000/api/products
   ```
   Should return JSON array

3. **Check browser Network tab:**
   - Open DevTools → Network tab
   - Navigate to Products page
   - Look for request to `http://localhost:5000/api/products`
   - Check status code (should be 200)
   - Check response (should be JSON array)

4. **Clear browser cache:**
   - Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)

---

## Expected Behavior

✅ **Working correctly:**
- Products page shows product cards
- Can see product names, prices, images
- Can filter by category
- Can search products

❌ **Not working:**
- Shows "Loading products..." forever
- Shows "No products found"
- Blank page
- Console shows errors

---

## Summary Checklist

- [ ] Backend dependencies installed: `pip install -r requirements.txt`
- [ ] Backend running: `python app.py` (port 5000)
- [ ] Frontend running: `npm start` (port 3000)
- [ ] API test works: http://localhost:5000/api/products shows JSON
- [ ] No errors in backend terminal
- [ ] No errors in browser console
- [ ] Database exists: `backend/ecommerce.db`

If all checked, products should display! 🎉

