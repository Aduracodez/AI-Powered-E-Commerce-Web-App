# CRUD Operations Tutorial - E-Commerce App

## What is CRUD?

**CRUD** stands for:
- **C**reate - Add new records
- **R**ead - Retrieve/View records
- **U**pdate - Modify existing records
- **D**elete - Remove records

These are the four fundamental operations for managing data in any application.

---

## 1. PRODUCTS - CRUD Operations

### CREATE (Adding Products)

#### Backend (Python/Flask)
```python
# Location: backend/app.py (lines 301-510)
# Products are created in the seed function when database is initialized

def create_tables():
    db.create_all()
    
    if Product.query.count() == 0:
        sample_products = [
            Product(
                name='Wireless Headphones',
                description='Premium wireless headphones',
                price=199.99,
                image_url='https://...',
                stock=50,
                category='Electronics'
            ),
            # ... more products
        ]
        db.session.add_all(sample_products)  # Add to session
        db.session.commit()  # Save to database
```

**Key Steps:**
1. Create a `Product` object with data
2. Add to database session: `db.session.add()` or `db.session.add_all()`
3. Commit to database: `db.session.commit()`

#### Frontend (React)
```javascript
// Example: Creating a product from frontend (not currently in app)
// This would be an admin feature

const createProduct = async (productData) => {
  try {
    const response = await axios.post('http://localhost:5000/api/products', {
      name: productData.name,
      description: productData.description,
      price: productData.price,
      image_url: productData.imageUrl,
      stock: productData.stock,
      category: productData.category
    });
    console.log('Product created:', response.data);
  } catch (error) {
    console.error('Error creating product:', error);
  }
};
```

**HTTP Method:** `POST`
**Endpoint:** `/api/products`

---

### READ (Viewing Products)

#### Backend
```python
# Location: backend/app.py (lines 105-139)

# Get ALL products (with optional filters)
@app.route('/api/products', methods=['GET'])
def get_products():
    category = request.args.get('category')  # Query parameter
    search = request.args.get('search')      # Query parameter
    
    query = Product.query  # Start with all products
    
    if category:
        query = query.filter_by(category=category)  # Filter by category
    if search:
        query = query.filter(
            Product.name.contains(search) | 
            Product.description.contains(search)
        )
    
    products = query.all()  # Execute query and get all results
    
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'description': p.description,
        'price': p.price,
        'image_url': p.image_url,
        'stock': p.stock,
        'category': p.category
    } for p in products]), 200

# Get SINGLE product by ID
@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)  # Get or return 404
    
    return jsonify({
        'id': product.id,
        'name': product.name,
        # ... other fields
    }), 200
```

**Key SQLAlchemy Methods:**
- `Product.query` - Start query
- `.all()` - Get all results
- `.get(id)` - Get by primary key
- `.get_or_404(id)` - Get or return 404 error
- `.filter_by(field=value)` - Filter by exact match
- `.filter(condition)` - Filter with custom condition

#### Frontend
```javascript
// Location: frontend/src/pages/Products.js (lines 16-30)

// READ ALL Products
const fetchProducts = async () => {
  try {
    setLoading(true);
    const params = {};
    if (category) params.category = category;
    if (search) params.search = search;
    
    // GET request with query parameters
    const response = await axios.get('http://localhost:5000/api/products', { 
      params 
    });
    setProducts(response.data);  // Update state with products
  } catch (error) {
    console.error('Error fetching products:', error);
  } finally {
    setLoading(false);
  }
};

// READ SINGLE Product
// Location: frontend/src/pages/ProductDetail.js (lines 20-29)
const fetchProduct = async () => {
  try {
    const response = await axios.get(
      `http://localhost:5000/api/products/${id}`
    );
    setProduct(response.data);
  } catch (error) {
    console.error('Error fetching product:', error);
  }
};
```

**HTTP Method:** `GET`
**Endpoints:** 
- `/api/products` (all products)
- `/api/products/<id>` (single product)

---

### UPDATE (Modifying Products)

#### Backend Example (Not currently implemented, but here's how):
```python
# This would be an admin endpoint
@app.route('/api/products/<int:product_id>', methods=['PUT'])
@jwt_required()  # Require authentication
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    
    # Update fields if provided
    if 'name' in data:
        product.name = data['name']
    if 'price' in data:
        product.price = data['price']
    if 'stock' in data:
        product.stock = data['stock']
    # ... update other fields
    
    db.session.commit()  # Save changes
    
    return jsonify({
        'message': 'Product updated successfully',
        'product': {
            'id': product.id,
            'name': product.name,
            # ... other fields
        }
    }), 200
```

**Key Steps:**
1. Get the product from database
2. Modify its attributes
3. Commit changes: `db.session.commit()`

#### Frontend Example:
```javascript
const updateProduct = async (productId, updates) => {
  try {
    const response = await axios.put(
      `http://localhost:5000/api/products/${productId}`,
      updates  // Data to update
    );
    console.log('Product updated:', response.data);
  } catch (error) {
    console.error('Error updating product:', error);
  }
};

// Usage
updateProduct(1, { price: 249.99, stock: 100 });
```

**HTTP Method:** `PUT` or `PATCH`

---

### DELETE (Removing Products)

#### Backend Example:
```python
@app.route('/api/products/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    db.session.delete(product)  # Mark for deletion
    db.session.commit()         # Remove from database
    
    return jsonify({'message': 'Product deleted successfully'}), 200
```

**Key Steps:**
1. Get the product
2. Delete: `db.session.delete(object)`
3. Commit: `db.session.commit()`

#### Frontend Example:
```javascript
const deleteProduct = async (productId) => {
  try {
    await axios.delete(`http://localhost:5000/api/products/${productId}`);
    console.log('Product deleted');
  } catch (error) {
    console.error('Error deleting product:', error);
  }
};
```

**HTTP Method:** `DELETE`

---

## 2. CART ITEMS - CRUD Operations

### CREATE (Add to Cart)

#### Backend
```python
# Location: backend/app.py (lines 159-176)

@app.route('/api/cart', methods=['POST'])
@jwt_required()  # Must be logged in
def add_to_cart():
    user_id = get_jwt_identity()  # Get user from JWT token
    data = request.get_json()
    
    product = Product.query.get_or_404(data['product_id'])
    
    # Check if item already in cart
    existing_item = CartItem.query.filter_by(
        user_id=user_id, 
        product_id=data['product_id']
    ).first()
    
    if existing_item:
        # UPDATE: Increase quantity (combining CREATE and UPDATE)
        existing_item.quantity += data.get('quantity', 1)
    else:
        # CREATE: Add new cart item
        cart_item = CartItem(
            user_id=user_id,
            product_id=data['product_id'],
            quantity=data.get('quantity', 1)
        )
        db.session.add(cart_item)
    
    db.session.commit()
    return jsonify({'message': 'Item added to cart'}), 201
```

#### Frontend
```javascript
// Location: frontend/src/pages/ProductDetail.js (lines 31-44)

// For logged-in users
const handleAddToCart = async () => {
  if (user) {
    try {
      await axios.post('http://localhost:5000/api/cart', {
        product_id: parseInt(id),
        quantity: quantity,
      });
      setMessage('Product added to cart!');
    } catch (error) {
      setMessage('Failed to add to cart');
    }
  } else {
    // Guest: Use localStorage (frontend-only)
    const guestCart = JSON.parse(localStorage.getItem('guestCart') || '[]');
    // ... add to localStorage
  }
};
```

---

### READ (View Cart)

#### Backend
```python
# Location: backend/app.py (lines 141-157)

@app.route('/api/cart', methods=['GET'])
@jwt_required()
def get_cart():
    user_id = get_jwt_identity()
    
    # READ: Get all cart items for this user
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    
    return jsonify([{
        'id': item.id,
        'product': {
            'id': item.product.id,
            'name': item.product.name,
            'price': item.product.price,
            # ... more product fields
        },
        'quantity': item.quantity
    } for item in cart_items]), 200
```

#### Frontend
```javascript
// Location: frontend/src/pages/Cart.js (lines 24-33)

const fetchCart = async () => {
  try {
    const response = await axios.get('http://localhost:5000/api/cart');
    setCartItems(response.data);
  } catch (error) {
    console.error('Error fetching cart:', error);
  }
};
```

---

### UPDATE (Change Quantity)

#### Backend
```python
# Location: backend/app.py (lines 178-188)

@app.route('/api/cart/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_cart_item(item_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Get cart item (only if it belongs to this user)
    cart_item = CartItem.query.filter_by(
        id=item_id, 
        user_id=user_id
    ).first_or_404()
    
    # UPDATE: Modify quantity
    cart_item.quantity = data['quantity']
    
    db.session.commit()
    return jsonify({'message': 'Cart item updated'}), 200
```

#### Frontend
```javascript
// Location: frontend/src/pages/Cart.js (lines 46-67)

const updateQuantity = async (itemId, newQuantity) => {
  if (newQuantity < 1) return;
  
  if (user) {
    try {
      await axios.put(`http://localhost:5000/api/cart/${itemId}`, {
        quantity: newQuantity,
      });
      fetchCart();  // Refresh cart
    } catch (error) {
      console.error('Error updating cart:', error);
    }
  } else {
    // Guest: Update localStorage
    const guestCart = JSON.parse(localStorage.getItem('guestCart') || '[]');
    const itemIndex = guestCart.findIndex(item => item.product_id === itemId);
    if (itemIndex >= 0) {
      guestCart[itemIndex].quantity = newQuantity;
      localStorage.setItem('guestCart', JSON.stringify(guestCart));
    }
  }
};
```

---

### DELETE (Remove from Cart)

#### Backend
```python
# Location: backend/app.py (lines 190-198)

@app.route('/api/cart/<int:item_id>', methods=['DELETE'])
@jwt_required()
def remove_from_cart(item_id):
    user_id = get_jwt_identity()
    
    # Get cart item
    cart_item = CartItem.query.filter_by(
        id=item_id, 
        user_id=user_id
    ).first_or_404()
    
    # DELETE: Remove from database
    db.session.delete(cart_item)
    db.session.commit()
    
    return jsonify({'message': 'Item removed from cart'}), 200
```

#### Frontend
```javascript
// Location: frontend/src/pages/Cart.js (lines 69-83)

const removeItem = async (itemId) => {
  if (user) {
    try {
      await axios.delete(`http://localhost:5000/api/cart/${itemId}`);
      fetchCart();  // Refresh cart
    } catch (error) {
      console.error('Error removing item:', error);
    }
  } else {
    // Guest: Remove from localStorage
    const guestCart = JSON.parse(localStorage.getItem('guestCart') || '[]');
    const filteredCart = guestCart.filter(item => item.product_id !== itemId);
    localStorage.setItem('guestCart', JSON.stringify(filteredCart));
  }
};
```

---

## 3. ORDERS - CRUD Operations

### CREATE (Place Order)

#### Backend
```python
# Location: backend/app.py (lines 200-280)

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    
    # Check if user is authenticated
    user_id = None
    try:
        user_id = get_jwt_identity()
    except:
        pass  # Guest order
    
    if not user_id:
        # Guest order
        items = data.get('items', [])
        total_amount = sum(item['price'] * item['quantity'] for item in items)
        
        # CREATE: New order
        order = Order(
            user_id=None,
            guest_email=data.get('email', ''),
            guest_name=data.get('name', ''),
            total_amount=total_amount,
            shipping_address=data.get('shipping_address', '')
        )
        db.session.add(order)
        db.session.flush()  # Get order.id without committing
        
        # CREATE: Order items
        for item in items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item['product_id'],
                quantity=item['quantity'],
                price=item['price']
            )
            db.session.add(order_item)
        
        db.session.commit()
    else:
        # Authenticated user order
        cart_items = CartItem.query.filter_by(user_id=user_id).all()
        total_amount = sum(item.product.price * item.quantity for item in cart_items)
        
        order = Order(
            user_id=user_id,
            total_amount=total_amount,
            shipping_address=data.get('shipping_address', '')
        )
        db.session.add(order)
        db.session.flush()
        
        for item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.product.price
            )
            db.session.add(order_item)
            db.session.delete(item)  # DELETE: Remove from cart
        
        db.session.commit()
    
    return jsonify({
        'message': 'Order created successfully',
        'order_id': order.id,
        'total_amount': order.total_amount
    }), 201
```

**Key Concepts:**
- `db.session.flush()` - Saves changes temporarily so you can use `order.id` before committing
- Multiple creates in one transaction
- Relationship handling (Order has many OrderItems)

#### Frontend
```javascript
// Location: frontend/src/pages/Cart.js (lines 85-130)

const handleCheckout = async () => {
  if (!shippingAddress.trim()) {
    alert('Please enter a shipping address');
    return;
  }

  if (user) {
    // Authenticated user
    try {
      const response = await axios.post('http://localhost:5000/api/orders', {
        shipping_address: shippingAddress,
      });
      alert('Order placed successfully!');
      navigate('/orders');
    } catch (error) {
      alert('Failed to place order');
    }
  } else {
    // Guest checkout
    const items = cartItems.map(item => ({
      product_id: item.product_id,
      quantity: item.quantity,
      price: item.product.price
    }));

    try {
      const response = await axios.post('http://localhost:5000/api/orders', {
        name: guestName,
        email: guestEmail,
        shipping_address: shippingAddress,
        items: items
      });
      
      localStorage.removeItem('guestCart');  // Clear cart
      alert(`Order placed! Order ID: ${response.data.order_id}`);
    } catch (error) {
      alert('Failed to place order');
    }
  }
};
```

---

### READ (View Orders)

#### Backend
```python
# Location: backend/app.py (lines 282-299)

@app.route('/api/orders', methods=['GET'])
@jwt_required()
def get_orders():
    user_id = get_jwt_identity()
    
    # READ: Get all orders for this user, ordered by date (newest first)
    orders = Order.query.filter_by(user_id=user_id).order_by(
        Order.created_at.desc()
    ).all()
    
    return jsonify([{
        'id': order.id,
        'total_amount': order.total_amount,
        'status': order.status,
        'shipping_address': order.shipping_address,
        'created_at': order.created_at.isoformat(),
        'items': [{
            'product_name': item.product.name,
            'quantity': item.quantity,
            'price': item.price
        } for item in order.items]  # Access related OrderItems
    } for order in orders]), 200
```

**Key SQLAlchemy Methods:**
- `.order_by(Order.created_at.desc())` - Sort by date descending
- `order.items` - Access related OrderItems via relationship

#### Frontend
```javascript
// Location: frontend/src/pages/Orders.js

const fetchOrders = async () => {
  try {
    const response = await axios.get('http://localhost:5000/api/orders');
    setOrders(response.data);
  } catch (error) {
    console.error('Error fetching orders:', error);
  }
};
```

---

### UPDATE (Not currently implemented, but would be for order status)

```python
# Example: Update order status
@app.route('/api/orders/<int:order_id>', methods=['PUT'])
@jwt_required()
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.get_json()
    
    # UPDATE: Change status
    order.status = data.get('status', order.status)
    
    db.session.commit()
    return jsonify({'message': 'Order updated'}), 200
```

---

### DELETE (Not typically used for orders - usually just update status to "cancelled")

```python
# Example: Cancel order (update status instead of delete)
@app.route('/api/orders/<int:order_id>/cancel', methods=['PUT'])
@jwt_required()
def cancel_order(order_id):
    order = Order.query.get_or_404(order_id)
    
    # UPDATE: Change status to cancelled
    order.status = 'cancelled'
    
    db.session.commit()
    return jsonify({'message': 'Order cancelled'}), 200
```

---

## 4. USERS - CRUD Operations

### CREATE (Register User)

#### Backend
```python
# Location: backend/app.py (lines 69-89)

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Check if username already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    # Check if email already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    # Hash password for security
    hashed_password = bcrypt.generate_password_hash(
        data['password']
    ).decode('utf-8')
    
    # CREATE: New user
    user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password
    )
    db.session.add(user)
    db.session.commit()
    
    # Generate JWT token for authentication
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'message': 'User created successfully',
        'access_token': access_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    }), 201
```

#### Frontend
```javascript
// Location: frontend/src/context/AuthContext.js (lines 40-59)

const register = async (username, email, password) => {
  try {
    const response = await axios.post('http://localhost:5000/api/register', {
      username,
      email,
      password,
    });
    const { access_token, user } = response.data;
    localStorage.setItem('token', access_token);  // Store token
    setToken(access_token);
    setUser(user);
    axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
    return { success: true };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.error || 'Registration failed',
    };
  }
};
```

---

### READ (Login/Get User Info)

#### Backend
```python
# Location: backend/app.py (lines 91-103)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # READ: Find user by username
    user = User.query.filter_by(username=data['username']).first()
    
    # Verify password
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({
            'access_token': access_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }), 200
    
    return jsonify({'error': 'Invalid username or password'}), 401
```

**Key Concepts:**
- Password hashing with bcrypt
- JWT token generation
- Authentication vs Authorization

---

## Database Relationships in CRUD

### One-to-Many Relationships

```python
# User has many CartItems
class User(db.Model):
    cart_items = db.relationship('CartItem', backref='user')

# Access cart items from user
user = User.query.get(1)
cart_items = user.cart_items  # Get all cart items

# Access user from cart item
cart_item = CartItem.query.get(1)
user = cart_item.user  # Get the user
```

### Many-to-Many (via Join Table)

```python
# Order has many OrderItems
# Each OrderItem references a Product

order = Order.query.get(1)
items = order.items  # Get all order items

for item in items:
    product = item.product  # Access related product
    print(product.name, item.quantity)
```

---

## HTTP Methods Summary

| Operation | HTTP Method | Example Endpoint | Purpose |
|-----------|-------------|------------------|---------|
| CREATE | POST | `/api/products` | Add new resource |
| READ (All) | GET | `/api/products` | Get all resources |
| READ (One) | GET | `/api/products/1` | Get single resource |
| UPDATE | PUT/PATCH | `/api/products/1` | Modify resource |
| DELETE | DELETE | `/api/products/1` | Remove resource |

---

## SQLAlchemy Query Patterns

```python
# CREATE
new_item = Model(field1=value1, field2=value2)
db.session.add(new_item)
db.session.commit()

# READ (All)
items = Model.query.all()

# READ (One by ID)
item = Model.query.get(id)

# READ (One or 404)
item = Model.query.get_or_404(id)

# READ (Filter)
items = Model.query.filter_by(field=value).all()

# READ (Filter with condition)
items = Model.query.filter(Model.field > value).all()

# READ (Multiple filters)
items = Model.query.filter_by(field1=value1).filter_by(field2=value2).all()

# UPDATE
item = Model.query.get(id)
item.field = new_value
db.session.commit()

# DELETE
item = Model.query.get(id)
db.session.delete(item)
db.session.commit()
```

---

## Frontend Axios Patterns

```javascript
// CREATE
await axios.post('/api/resource', { data });

// READ (All)
const response = await axios.get('/api/resource');
const items = response.data;

// READ (One)
const response = await axios.get(`/api/resource/${id}`);
const item = response.data;

// READ (With query params)
const response = await axios.get('/api/resource', {
  params: { category: 'Electronics', search: 'phone' }
});

// UPDATE
await axios.put(`/api/resource/${id}`, { field: newValue });

// DELETE
await axios.delete(`/api/resource/${id}`);
```

---

## Best Practices

1. **Always validate data** before creating/updating
2. **Use transactions** for multiple related operations
3. **Handle errors** properly in both backend and frontend
4. **Use proper HTTP status codes** (200, 201, 400, 401, 404, 500)
5. **Authenticate** when necessary (`@jwt_required()`)
6. **Filter by user** to prevent unauthorized access
7. **Use relationships** to access related data efficiently

---

## Practice Exercises

Try implementing these:

1. **Product Management Admin Panel**
   - Create: Add new products
   - Update: Edit product details
   - Delete: Remove products

2. **Order Status Management**
   - Update: Change order status (pending → processing → shipped)

3. **User Profile Management**
   - Read: View user profile
   - Update: Edit profile information

Good luck learning CRUD operations! 🚀

