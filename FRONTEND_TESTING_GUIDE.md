# Frontend Testing Guide - 👑 The Queens

## 🚀 Quick Start

### Step 1: Start Backend Server

**Option A: Flask Backend (Port 5000)**
```bash
cd backend
python app.py
```

**Option B: Django Backend (Port 8000)**
```bash
cd backend_django
source venv/bin/activate
python manage.py runserver
```

✅ You should see: `* Running on http://127.0.0.1:5000` or `http://127.0.0.1:8000`

### Step 2: Start Frontend Server

**Open a NEW terminal:**
```bash
cd frontend
npm start
```

✅ Frontend will open automatically at: **http://localhost:3000**

---

## 🧪 Testing Checklist

### ✅ Test 1: Home Page

**What to test:**
1. Open http://localhost:3000
2. Verify the page loads
3. Check navigation bar shows "👑 The Queens"
4. See hero section with "Welcome to The Queens 👑"
5. Click "Shop Now" button → Should navigate to Products page

**Expected Result:**
- ✅ Page loads without errors
- ✅ Store name displays correctly
- ✅ Navigation works

---

### ✅ Test 2: Browse Products

**Steps:**
1. Click "Products" in navigation OR click "Shop Now" button
2. Wait for products to load

**Expected Result:**
- ✅ See 50 products displayed in a grid
- ✅ Each product card shows:
  - Product image
  - Product name
  - Description
  - Price
  - Stock status (In Stock/Out of Stock)

**If products don't load:**
- Check browser console (F12) for errors
- Verify backend is running
- Check API: http://localhost:8000/api/products/ (Django) or http://localhost:5000/api/products (Flask)

---

### ✅ Test 3: Product Filtering

**Steps:**
1. On Products page, click category filter buttons:
   - "All" → Shows all products
   - "Electronics" → Shows only electronics (16 products)
   - "Fashion" → Shows only fashion items (8 products)
   - "Home" → Shows only home items (9 products)
   - "Fitness" → Shows only fitness items (9 products)
   - "Accessories" → Shows only accessories (8 products)

**Expected Result:**
- ✅ Clicking category filters the products
- ✅ Active filter button is highlighted
- ✅ Product count changes based on category

---

### ✅ Test 4: Search Products

**Steps:**
1. Type in the search box (e.g., "laptop", "shoes", "watch")
2. Products should filter as you type

**Expected Result:**
- ✅ Search filters products by name or description
- ✅ Results update in real-time
- ✅ Can search across all categories

---

### ✅ Test 5: Product Detail Page

**Steps:**
1. Click on any product card
2. Product detail page opens

**Expected Result:**
- ✅ See large product image
- ✅ See full product description
- ✅ See price
- ✅ See stock information
- ✅ Quantity selector works (+ and - buttons)
- ✅ "Add to Cart" button is visible

---

### ✅ Test 6: Guest User - Add to Cart

**Steps (as Guest - not logged in):**
1. Browse to a product detail page
2. Select quantity (if needed)
3. Click "Add to Cart"
4. Should see success message: "Product added to cart!"
5. Click "Cart" in navigation

**Expected Result:**
- ✅ Product added to cart
- ✅ Cart page shows the product
- ✅ Can see quantity, price, and total
- ✅ Cart persists in localStorage (refreshing page keeps items)

---

### ✅ Test 7: Guest User - Cart Management

**Steps:**
1. Go to Cart page
2. Test quantity controls:
   - Click "+" to increase quantity
   - Click "-" to decrease quantity
   - Quantity should update
3. Click "×" to remove item

**Expected Result:**
- ✅ Quantity updates work
- ✅ Total price recalculates
- ✅ Remove button deletes item from cart
- ✅ "Shopping as Guest" indicator shows

---

### ✅ Test 8: Guest Checkout

**Steps:**
1. Add items to cart (as guest)
2. Go to Cart page
3. Fill in checkout form:
   - **Name:** Enter your name
   - **Email:** Enter email address
   - **Shipping Address:** Enter delivery address
4. Click "Place Order as Guest"

**Expected Result:**
- ✅ Order placed successfully
- ✅ See order confirmation with Order ID
- ✅ Cart is cleared
- ✅ Redirected to Products page

---

### ✅ Test 9: User Registration

**Steps:**
1. Click "Sign Up" or "Login" → "Sign up" link
2. Fill registration form:
   - Username (unique)
   - Email (unique)
   - Password (min 6 characters)
   - Confirm Password
3. Click "Sign Up"

**Expected Result:**
- ✅ Account created successfully
- ✅ Automatically logged in
- ✅ See "Hello, [username]" in navigation
- ✅ Redirected to home page

---

### ✅ Test 10: User Login

**Steps:**
1. Click "Login" in navigation
2. Enter username and password
3. Click "Login"

**Expected Result:**
- ✅ Login successful
- ✅ See "Hello, [username]" in navigation
- ✅ "Orders" link appears in navigation
- ✅ Cart shows backend-stored items (if any)

---

### ✅ Test 11: Authenticated User - Add to Cart

**Steps (while logged in):**
1. Browse products
2. Add items to cart
3. Go to Cart page

**Expected Result:**
- ✅ Items stored in backend database
- ✅ Cart persists across sessions
- ✅ Can see all items with correct quantities

---

### ✅ Test 12: Authenticated User - Checkout

**Steps:**
1. Add items to cart (while logged in)
2. Go to Cart page
3. Enter shipping address
4. Click "Proceed to Checkout"

**Expected Result:**
- ✅ Order created successfully
- ✅ Cart is cleared
- ✅ Redirected to Orders page

---

### ✅ Test 13: View Order History

**Steps (must be logged in):**
1. Click "Orders" in navigation
2. View order history

**Expected Result:**
- ✅ See all previous orders
- ✅ Order details include:
  - Order ID
  - Order date
  - Total amount
  - Status (pending, shipped, etc.)
  - Shipping address
  - List of items in each order

---

### ✅ Test 14: Navigation

**Test all navigation links:**
- ✅ "Home" → Goes to home page
- ✅ "Products" → Goes to products page
- ✅ "Cart" → Goes to cart (works for guests and users)
- ✅ "Orders" → Goes to orders (only when logged in)
- ✅ "Login" → Goes to login page (when logged out)
- ✅ "Sign Up" → Goes to registration page (when logged out)
- ✅ "Logout" → Logs out and redirects to home

**Expected Result:**
- ✅ All links work correctly
- ✅ Navigation shows/hides based on login status

---

### ✅ Test 15: Responsive Design

**Steps:**
1. Open browser DevTools (F12)
2. Click device toolbar icon (or press Ctrl+Shift+M / Cmd+Shift+M)
3. Test on different screen sizes:
   - Mobile (375px width)
   - Tablet (768px width)
   - Desktop (1920px width)

**Expected Result:**
- ✅ Layout adapts to screen size
- ✅ Products grid stacks on mobile
- ✅ Navigation menu works on mobile
- ✅ Text is readable on all sizes

---

## 🐛 Troubleshooting Tests

### Products Not Showing?

**Check 1: Backend is running**
```bash
# Test Flask
curl http://localhost:5000/api/products

# Test Django
curl http://localhost:8000/api/products/
```

**Check 2: Browser Console**
- Press F12 → Console tab
- Look for red error messages
- Common errors:
  - `ECONNREFUSED` → Backend not running
  - `CORS error` → Backend CORS not configured
  - `404` → Wrong API URL

**Check 3: Network Tab**
- Press F12 → Network tab
- Click "Products" page
- Look for request to `/api/products`
- Check status code (should be 200)
- Check response (should be JSON array)

---

### Cart Not Working?

**For Guests:**
- Cart stored in localStorage
- Check browser DevTools → Application → Local Storage
- Should see `guestCart` key with items

**For Logged-in Users:**
- Cart stored in backend database
- Must be logged in
- Check backend terminal for errors

---

### Can't Login/Register?

**Check:**
1. Backend is running
2. No errors in browser console
3. Using correct credentials
4. Username/email is unique (for registration)

**Test API directly:**
```bash
# Test registration
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@test.com","password":"test123","password2":"test123"}'

# Test login
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"test123"}'
```

---

## 📋 Complete Test Scenarios

### Scenario 1: Guest Shopping Flow

1. ✅ Visit homepage
2. ✅ Browse products
3. ✅ Filter by category
4. ✅ Search for product
5. ✅ View product details
6. ✅ Add 3 different products to cart
7. ✅ View cart
8. ✅ Update quantities
9. ✅ Remove one item
10. ✅ Fill checkout form (name, email, address)
11. ✅ Place order as guest
12. ✅ Verify order confirmation

---

### Scenario 2: Registered User Flow

1. ✅ Register new account
2. ✅ Login
3. ✅ Browse products
4. ✅ Add items to cart
5. ✅ View cart
6. ✅ Place order
7. ✅ View order history
8. ✅ Logout
9. ✅ Login again
10. ✅ Verify cart persists (if not checked out)
11. ✅ Verify order history still visible

---

## 🎯 Quick Test Commands

### Test Backend API (Terminal)

```bash
# Get all products
curl http://localhost:8000/api/products/

# Get single product
curl http://localhost:8000/api/products/1/

# Search products
curl "http://localhost:8000/api/products/?search=laptop"

# Filter by category
curl "http://localhost:8000/api/products/?category=Electronics"
```

### Test Frontend (Browser)

1. Open: http://localhost:3000
2. Press F12 (DevTools)
3. Console tab → Check for errors
4. Network tab → Monitor API calls
5. Application tab → Check localStorage for guest cart

---

## ✅ Success Criteria

Your app is working correctly if:

- ✅ All 50 products display
- ✅ Category filtering works
- ✅ Search works
- ✅ Product detail pages load
- ✅ Guest can add to cart
- ✅ Guest can checkout
- ✅ User registration works
- ✅ User login works
- ✅ Authenticated user cart works
- ✅ Order creation works
- ✅ Order history displays
- ✅ Navigation works
- ✅ Responsive design works
- ✅ Dark theme displays correctly

---

## 🎉 Ready to Test!

1. **Start Backend:** `cd backend_django && source venv/bin/activate && python manage.py runserver`
2. **Start Frontend:** `cd frontend && npm start`
3. **Open Browser:** http://localhost:3000
4. **Start Testing!** 🚀

Follow the test scenarios above to verify everything works!

