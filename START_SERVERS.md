# 🚀 Start Your E-commerce Store

## ✅ Quick Start Guide

### Step 1: Start Backend (Django)

Open Terminal 1:
```bash
cd backend_django
source venv/bin/activate
python manage.py runserver 8001
```

**Expected output:**
```
Starting development server at http://127.0.0.1:8001/
Quit the server with CONTROL-C.
```

### Step 2: Verify Backend is Running

Open Terminal 2 (new terminal):
```bash
curl http://localhost:8001/api/products/
```

**Expected:** Should return JSON with products list like:
```json
{
  "count": 50,
  "next": null,
  "previous": null,
  "results": [...]
}
```

If you get an error, check:
- Is the backend running? (Step 1)
- Is the database seeded? (Step 3)

### Step 3: Seed Database (if needed)

If products don't appear, seed the database:

```bash
cd backend_django
source venv/bin/activate
python manage.py seed_products
```

**Expected output:**
```
Products seeded successfully: 50 products created
```

### Step 4: Start Frontend (React)

Open Terminal 3 (new terminal):
```bash
cd frontend
npm start
```

**Expected:** Browser opens automatically to http://localhost:3001

## 🔍 Troubleshooting

### Products Not Displaying?

1. **Check Backend is Running:**
   ```bash
   lsof -i :8001 | grep LISTEN
   ```
   Should show Python process

2. **Check Browser Console:**
   - Open DevTools (F12 or Cmd+Option+I)
   - Go to Console tab
   - Look for error messages
   - Check for "📦 Products API Response" log

3. **Check Network Tab:**
   - Open DevTools → Network tab
   - Refresh page
   - Look for `/api/products/` request
   - Check status code (should be 200)
   - Check response format

4. **Test API Directly:**
   ```bash
   curl http://localhost:8001/api/products/ | python3 -m json.tool | head -20
   ```

5. **Verify Database Has Products:**
   ```bash
   cd backend_django
   source venv/bin/activate
   python manage.py shell
   ```
   Then in Python shell:
   ```python
   from api.models import Product
   print(f"Total products: {Product.objects.count()}")
   Product.objects.all()[:5]  # Show first 5
   exit()
   ```

### Backend Won't Start?

- **Port 8001 already in use?**
  ```bash
  lsof -i :8001
  kill -9 <PID>
  ```

- **Virtual environment not activated?**
  ```bash
  cd backend_django
  source venv/bin/activate
  ```

- **Dependencies not installed?**
  ```bash
  cd backend_django
  source venv/bin/activate
  pip install -r requirements.txt
  ```

### Frontend Won't Start?

- **Port 3001 already in use?**
  ```bash
  lsof -i :3001
  kill -9 <PID>
  ```

- **Dependencies not installed?**
  ```bash
  cd frontend
  npm install
  ```

## 📝 Ports Summary

- **Frontend:** http://localhost:3001
- **Backend API:** http://localhost:8001/api/

## 🎯 Access Your Store

Once both servers are running:
👉 **http://localhost:3001**

---

## 💡 Pro Tips

1. **Keep both terminals open** - Backend and Frontend need to run simultaneously
2. **Check console logs** - Frontend now logs product API responses for debugging
3. **Use browser DevTools** - Network tab shows API calls, Console shows errors
4. **Test API directly** - Use `curl` to verify backend works independently

