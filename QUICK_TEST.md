# Quick Frontend Testing Guide

## 🚀 3-Step Quick Start

### Step 1: Start Backend
```bash
# Django (recommended - already set up)
cd backend_django
source venv/bin/activate
python manage.py runserver
```

### Step 2: Start Frontend  
```bash
# In a NEW terminal
cd frontend
npm start
```

### Step 3: Open Browser
Visit: **http://localhost:3000**

---

## ✅ Basic Tests (5 minutes)

### Test 1: Homepage
- ✅ Opens at http://localhost:3000
- ✅ Shows "Welcome to The Queens 👑"
- ✅ Navigation bar visible

### Test 2: Products Page
1. Click "Products" in navigation
2. Should see **50 products** in a grid
3. Each product shows: image, name, price, stock

### Test 3: Product Details
1. Click any product card
2. Should see full product page with:
   - Large image
   - Full description
   - Price
   - Quantity selector
   - "Add to Cart" button

### Test 4: Add to Cart (Guest)
1. Go to product detail page
2. Click "Add to Cart"
3. Should see success message
4. Click "Cart" in navigation
5. Should see your product in cart

### Test 5: Guest Checkout
1. Add products to cart (as guest)
2. Go to Cart page
3. Fill form:
   - Name: Your name
   - Email: your@email.com
   - Shipping Address: Your address
4. Click "Place Order as Guest"
5. Should see order confirmation

---

## 🔐 User Account Tests

### Register
1. Click "Sign Up"
2. Fill form (username, email, password)
3. Click "Sign Up"
4. Should be logged in automatically

### Login
1. Click "Login"
2. Enter credentials
3. Click "Login"
4. Should see "Hello, [username]"

### View Orders (Logged In)
1. Login
2. Click "Orders" in navigation
3. Should see order history page

---

## 🎨 Visual Checks

### Dark Theme
- ✅ Dark background (#0a0a0a)
- ✅ Light text (#e0e0e0)
- ✅ Cyan accent color (#00d4ff)
- ✅ Cards have dark background

### Responsive
- Press F12 → Device Toolbar (or Ctrl+Shift+M)
- Resize window
- ✅ Layout adapts to screen size
- ✅ Products grid stacks on mobile

---

## 🐛 Quick Troubleshooting

### No Products Showing?
```bash
# Check backend is running
curl http://localhost:8000/api/products/
```

Should return JSON array. If empty or error:
```bash
cd backend_django
source venv/bin/activate
python manage.py seed_products
```

### Frontend Won't Start?
```bash
cd frontend
npm install
npm start
```

### Backend Errors?
Check terminal where backend is running for error messages.

---

## 📊 What You Should See

### Products Page
- Grid of product cards
- Category filter buttons at top
- Search box
- 50 products total

### Product Card
- Product image (or placeholder)
- Product name
- Short description
- Price (e.g., "$199.99")
- Stock badge ("In Stock" or "Out of Stock")

### Cart Page
- List of cart items
- Quantity controls (+/-)
- Remove button (×)
- Order summary
- Checkout form
- Total price

---

## ✅ Checklist

- [ ] Backend server running (port 5000 or 8000)
- [ ] Frontend server running (port 3000)
- [ ] Browser shows http://localhost:3000
- [ ] Homepage loads
- [ ] Products page shows 50 products
- [ ] Can click on product to see details
- [ ] Can add products to cart
- [ ] Can view cart
- [ ] Can place order (guest or logged in)
- [ ] Can register account
- [ ] Can login
- [ ] Can view orders (when logged in)

---

**That's it! Your frontend is ready to test! 🎉**

Just start both servers and open the browser - everything should work automatically!

