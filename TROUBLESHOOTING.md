# Troubleshooting: Products Not Showing

## Quick Fix Steps

### Step 1: Make sure backend is running

```bash
cd backend
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

### Step 2: Check if database was created

```bash
cd backend
ls -la *.db
```

If no `.db` file exists, the backend needs to run first to create it.

### Step 3: Test the API endpoint

Open your browser or use curl:
```bash
curl http://localhost:5000/api/products
```

Or open in browser: http://localhost:5000/api/products

You should see a JSON array of products.

### Step 4: Check browser console

Open browser DevTools (F12) → Console tab
Look for any errors like:
- `Network Error`
- `CORS policy`
- `Failed to fetch`

### Step 5: Check frontend is running

```bash
cd frontend
npm start
```

Should be running on: http://localhost:3000

---

## Common Issues & Solutions

### Issue 1: Backend not running
**Symptom:** Products page shows "Loading products..." forever or "No products found"

**Solution:**
1. Start the backend server:
```bash
cd backend
python app.py
```

### Issue 2: CORS Error
**Symptom:** Console shows `Access to XMLHttpRequest...has been blocked by CORS policy`

**Solution:** 
The backend already has CORS enabled. Make sure:
- Backend is running on port 5000
- Frontend is running on port 3000
- CORS is enabled in `app.py`: `CORS(app)`

### Issue 3: Database not seeded
**Symptom:** API returns `[]` (empty array)

**Solution:**
1. Stop the backend (Ctrl+C)
2. Delete the database file:
```bash
cd backend
rm -f ecommerce.db
```
3. Restart the backend - it will recreate the database and seed products

### Issue 4: Wrong API URL
**Symptom:** Network error in console

**Solution:** 
Check `frontend/src/pages/Products.js` line 23:
```javascript
const response = await axios.get('http://localhost:5000/api/products', { params });
```

Make sure:
- URL is correct: `http://localhost:5000`
- Backend is running on port 5000
- No firewall blocking the connection

### Issue 5: Products page shows "No products found"
**Possible causes:**
1. Database is empty - restart backend to reseed
2. Filters are active - click "All" button to reset
3. Search is filtering out everything - clear search box

---

## Manual Database Check

### Option 1: Python script
Create `backend/check_db.py`:
```python
from app import app, db, Product

with app.app_context():
    count = Product.query.count()
    print(f"Total products in database: {count}")
    
    if count > 0:
        products = Product.query.all()
        for p in products[:5]:
            print(f"- {p.name} (${p.price})")
    else:
        print("Database is empty. Need to seed products.")
```

Run: `python check_db.py`

### Option 2: Use Flask shell
```bash
cd backend
python
>>> from app import app, db, Product
>>> with app.app_context():
...     print(Product.query.count())
```

---

## Verification Checklist

- [ ] Backend server is running (port 5000)
- [ ] Frontend server is running (port 3000)
- [ ] Database file exists: `backend/ecommerce.db`
- [ ] API endpoint works: http://localhost:5000/api/products
- [ ] No CORS errors in browser console
- [ ] No network errors in browser console
- [ ] Products page is at: http://localhost:3000/products
- [ ] Database has products (check with curl or browser)

---

## Still Not Working?

1. Check backend terminal for errors
2. Check frontend terminal for errors
3. Check browser console (F12)
4. Check Network tab in DevTools - see if API call is being made
5. Verify backend logs show the GET request for `/api/products`

