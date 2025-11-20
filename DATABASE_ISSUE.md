# Database Issue Analysis

## 🔍 Problem Identified

**The database file `ecommerce.db` does not exist yet!**

### Root Cause

The database is created **only when the Flask backend server runs for the first time**. 

The database file `ecommerce.db` will be created in the `backend/` directory when:
1. You run `python app.py` 
2. Flask initializes and calls `create_tables()`
3. SQLAlchemy creates the database file and tables
4. Products are automatically seeded

---

## 🔧 Solution

### Step 1: Make sure you're in the backend directory
```bash
cd backend
```

### Step 2: Start the backend server
```bash
python app.py
```

OR

```bash
python3 app.py
```

**What happens when you start the backend:**

1. Flask app starts
2. `if __name__ == '__main__':` block runs
3. `create_tables()` function is called
4. Database file `ecommerce.db` is created
5. All tables are created (User, Product, CartItem, Order, OrderItem)
6. If database is empty, 20 products are automatically added

**Expected output:**
```
 * Running on http://127.0.0.1:5000
 * Restarting with stat
```

### Step 3: Verify database was created
```bash
# In a new terminal
cd backend
ls -la ecommerce.db
```

You should see:
```
-rw-r--r--  1 user  staff  123456  Jan 15 10:30 ecommerce.db
```

### Step 4: Verify products exist
Open your browser and go to:
```
http://localhost:5000/api/products
```

You should see JSON array with 20 products.

---

## 📊 Database Configuration

The database is configured in `backend/app.py`:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///ecommerce.db')
```

**What this means:**
- Database type: SQLite (file-based database)
- Location: `backend/ecommerce.db` (relative to where Python runs)
- File path: `sqlite:///ecommerce.db` creates file in current directory

---

## 🗂️ Database Structure

When created, the database will have these tables:

1. **user** - User accounts
   - id, username, email, password, created_at

2. **product** - Products catalog
   - id, name, description, price, image_url, stock, category, created_at

3. **cart_item** - Shopping cart items
   - id, user_id, product_id, quantity, created_at

4. **order** - Customer orders
   - id, user_id, guest_email, guest_name, total_amount, status, shipping_address, created_at

5. **order_item** - Items in each order
   - id, order_id, product_id, quantity, price

---

## 🚨 Common Issues

### Issue 1: Database file doesn't exist
**Symptom:** Products not showing in frontend

**Cause:** Backend hasn't been started yet

**Solution:**
```bash
cd backend
python app.py
```

### Issue 2: Database exists but is empty
**Symptom:** API returns `[]` (empty array)

**Cause:** Database was created but products weren't seeded

**Solution:**
```bash
cd backend
rm -f ecommerce.db  # Delete empty database
python app.py       # Restart - will recreate and seed
```

### Issue 3: Permission errors
**Symptom:** Cannot create database file

**Cause:** Directory permissions issue

**Solution:**
```bash
cd backend
chmod 755 .  # Give write permissions
python app.py
```

### Issue 4: Database locked
**Symptom:** Error: "database is locked"

**Cause:** Another process is using the database or previous server didn't shut down properly

**Solution:**
```bash
# Make sure all Python processes are stopped
pkill -f "python.*app.py"

# Wait a moment, then restart
python app.py
```

### Issue 5: Running from wrong directory
**Symptom:** Database created in wrong location

**Cause:** Running `python app.py` from wrong directory

**Solution:**
Always run from `backend/` directory:
```bash
cd /Users/preciousoladapo/Desktop/E_commerce_website/backend
python app.py
```

---

## ✅ Verification Steps

### Check 1: Database file exists
```bash
cd backend
ls -la ecommerce.db
```

### Check 2: Database has products
```bash
cd backend
python3 -c "
from app import app, db, Product
with app.app_context():
    count = Product.query.count()
    print(f'Products in database: {count}')
"
```

**Expected:** Should print `Products in database: 20`

### Check 3: API returns products
Open browser: `http://localhost:5000/api/products`

**Expected:** JSON array with products

### Check 4: Check database tables
```bash
cd backend
python3 -c "
import sqlite3
conn = sqlite3.connect('ecommerce.db')
cursor = conn.cursor()
cursor.execute(\"SELECT name FROM sqlite_master WHERE type='table';\")
print('Tables:', cursor.fetchall())
"
```

**Expected:** `Tables: [('user',), ('product',), ('cart_item',), ('order',), ('order_item',)]`

---

## 🔄 Recreating Database

If you need to start fresh:

```bash
cd backend

# Stop the backend server (Ctrl+C)

# Delete old database
rm -f ecommerce.db

# Start backend - it will recreate everything
python app.py
```

This will:
1. Create new `ecommerce.db` file
2. Create all tables
3. Seed with 20 products

---

## 📝 Summary

**The issue:** Database file doesn't exist because the backend hasn't been run yet.

**The fix:** 
1. Start the backend server: `cd backend && python app.py`
2. Database will be created automatically
3. Products will be seeded automatically
4. Frontend can now fetch products

**Database location:** `backend/ecommerce.db`

**When created:** First time you run `python app.py`

---

## 🎯 Quick Fix Command

Run these commands in order:

```bash
# Terminal 1: Start Backend
cd /Users/preciousoladapo/Desktop/E_commerce_website/backend
python app.py

# Terminal 2: Start Frontend (after backend is running)
cd /Users/preciousoladapo/Desktop/E_commerce_website/frontend
npm start
```

The database will be created when you run the backend! 🎉

