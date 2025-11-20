# CRUD Operations - Quick Reference Examples

## Visual CRUD Flow

```
┌─────────────────────────────────────────────────────────┐
│                    CREATE (POST)                        │
├─────────────────────────────────────────────────────────┤
│ Frontend → Send data → Backend → Save to DB → Response │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                    READ (GET)                           │
├─────────────────────────────────────────────────────────┤
│ Frontend → Request → Backend → Query DB → Return data  │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                    UPDATE (PUT)                         │
├─────────────────────────────────────────────────────────┤
│ Frontend → Send changes → Backend → Modify DB → Save   │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                    DELETE (DELETE)                      │
├─────────────────────────────────────────────────────────┤
│ Frontend → Request → Backend → Remove from DB → Confirm│
└─────────────────────────────────────────────────────────┘
```

---

## 1. PRODUCTS - Complete CRUD Example

### CREATE a Product

**Backend Request:**
```http
POST /api/products
Content-Type: application/json
Authorization: Bearer <token>

{
  "name": "iPhone 15",
  "description": "Latest iPhone with advanced camera",
  "price": 999.99,
  "image_url": "https://example.com/iphone.jpg",
  "stock": 50,
  "category": "Electronics"
}
```

**Backend Response:**
```json
{
  "message": "Product created successfully",
  "product": {
    "id": 21,
    "name": "iPhone 15",
    "price": 999.99,
    ...
  }
}
```

**Frontend Code:**
```javascript
const createProduct = async () => {
  const newProduct = {
    name: "iPhone 15",
    description: "Latest iPhone",
    price: 999.99,
    image_url: "https://example.com/iphone.jpg",
    stock: 50,
    category: "Electronics"
  };

  try {
    const response = await axios.post('/api/products', newProduct);
    console.log('Created:', response.data);
  } catch (error) {
    console.error('Error:', error.response.data);
  }
};
```

---

### READ Products

**Backend Request:**
```http
GET /api/products?category=Electronics&search=phone
```

**Backend Response:**
```json
[
  {
    "id": 1,
    "name": "Smartphone",
    "price": 799.99,
    "stock": 60,
    "category": "Electronics"
  },
  {
    "id": 2,
    "name": "iPhone 15",
    "price": 999.99,
    "stock": 50,
    "category": "Electronics"
  }
]
```

**Frontend Code:**
```javascript
// READ ALL with filters
const fetchProducts = async () => {
  const response = await axios.get('/api/products', {
    params: { category: 'Electronics', search: 'phone' }
  });
  setProducts(response.data);
};

// READ ONE
const fetchProduct = async (id) => {
  const response = await axios.get(`/api/products/${id}`);
  setProduct(response.data);
};
```

---

### UPDATE a Product

**Backend Request:**
```http
PUT /api/products/21
Content-Type: application/json
Authorization: Bearer <token>

{
  "price": 899.99,
  "stock": 75
}
```

**Backend Code:**
```python
@app.route('/api/products/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    
    # Update only provided fields
    if 'name' in data:
        product.name = data['name']
    if 'price' in data:
        product.price = data['price']
    if 'stock' in data:
        product.stock = data['stock']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Product updated',
        'product': {'id': product.id, 'name': product.name, ...}
    }), 200
```

**Frontend Code:**
```javascript
const updateProduct = async (productId, updates) => {
  try {
    const response = await axios.put(
      `/api/products/${productId}`,
      { price: 899.99, stock: 75 }
    );
    console.log('Updated:', response.data);
  } catch (error) {
    console.error('Error:', error);
  }
};
```

---

### DELETE a Product

**Backend Request:**
```http
DELETE /api/products/21
Authorization: Bearer <token>
```

**Backend Code:**
```python
@app.route('/api/products/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    db.session.delete(product)
    db.session.commit()
    
    return jsonify({'message': 'Product deleted'}), 200
```

**Frontend Code:**
```javascript
const deleteProduct = async (productId) => {
  try {
    await axios.delete(`/api/products/${productId}`);
    console.log('Product deleted');
    // Refresh the product list
    fetchProducts();
  } catch (error) {
    console.error('Error:', error);
  }
};
```

---

## 2. CART - CRUD Examples

### CREATE (Add to Cart)

**Backend Request:**
```http
POST /api/cart
Authorization: Bearer <token>
Content-Type: application/json

{
  "product_id": 5,
  "quantity": 2
}
```

**Database State Before:**
```
CartItem table:
[empty]
```

**Database State After:**
```
CartItem table:
| id | user_id | product_id | quantity |
|----|---------|------------|----------|
| 1  | 1       | 5          | 2        |
```

**Frontend Code:**
```javascript
// Adding item to cart
const addToCart = async (productId, quantity) => {
  await axios.post('/api/cart', {
    product_id: productId,
    quantity: quantity
  });
};
```

---

### READ (View Cart)

**Backend Request:**
```http
GET /api/cart
Authorization: Bearer <token>
```

**Backend Response:**
```json
[
  {
    "id": 1,
    "product": {
      "id": 5,
      "name": "Wireless Headphones",
      "price": 199.99,
      "image_url": "..."
    },
    "quantity": 2
  },
  {
    "id": 2,
    "product": {
      "id": 10,
      "name": "Laptop",
      "price": 1299.99
    },
    "quantity": 1
  }
]
```

---

### UPDATE (Change Quantity)

**Backend Request:**
```http
PUT /api/cart/1
Authorization: Bearer <token>
Content-Type: application/json

{
  "quantity": 3
}
```

**Database State:**
```
Before: | id | quantity |
        |----|----------|
        | 1  | 2        |

After:  | id | quantity |
        |----|----------|
        | 1  | 3        |
```

**Frontend Code:**
```javascript
const updateQuantity = async (cartItemId, newQuantity) => {
  await axios.put(`/api/cart/${cartItemId}`, {
    quantity: newQuantity
  });
  fetchCart(); // Refresh cart display
};
```

---

### DELETE (Remove from Cart)

**Backend Request:**
```http
DELETE /api/cart/1
Authorization: Bearer <token>
```

**Database State:**
```
Before:
CartItem table:
| id | user_id | product_id | quantity |
|----|---------|------------|----------|
| 1  | 1       | 5          | 2        |
| 2  | 1       | 10         | 1        |

After:
CartItem table:
| id | user_id | product_id | quantity |
|----|---------|------------|----------|
| 2  | 1       | 10         | 1        |
```

**Frontend Code:**
```javascript
const removeFromCart = async (cartItemId) => {
  await axios.delete(`/api/cart/${cartItemId}`);
  fetchCart(); // Refresh cart display
};
```

---

## 3. ORDERS - CRUD Examples

### CREATE (Place Order)

**Backend Request:**
```http
POST /api/orders
Authorization: Bearer <token>
Content-Type: application/json

{
  "shipping_address": "123 Main St, City, State 12345"
}
```

**What Happens:**
1. Get all cart items for user
2. Calculate total amount
3. **CREATE** new Order record
4. **CREATE** OrderItem records for each cart item
5. **DELETE** all cart items (clear cart)

**Database Changes:**
```
Before:
CartItem: [3 items]
Order: [empty]

After:
CartItem: [empty]
Order: [1 new order]
OrderItem: [3 items linked to order]
```

---

### READ (View Orders)

**Backend Request:**
```http
GET /api/orders
Authorization: Bearer <token>
```

**Backend Response:**
```json
[
  {
    "id": 1,
    "total_amount": 1799.97,
    "status": "pending",
    "created_at": "2024-01-15T10:30:00",
    "items": [
      {
        "product_name": "Wireless Headphones",
        "quantity": 2,
        "price": 199.99
      },
      {
        "product_name": "Laptop",
        "quantity": 1,
        "price": 1299.99
      }
    ]
  },
  {
    "id": 2,
    "total_amount": 299.99,
    "status": "shipped",
    ...
  }
]
```

---

## Real-World CRUD Flow Example

### Scenario: User buying a product

```
1. READ - User browses products
   GET /api/products
   → Shows product list

2. READ - User clicks on product
   GET /api/products/5
   → Shows product details

3. CREATE - User adds to cart
   POST /api/cart { product_id: 5, quantity: 2 }
   → Item added to cart

4. READ - User views cart
   GET /api/cart
   → Shows cart items

5. UPDATE - User changes quantity
   PUT /api/cart/1 { quantity: 3 }
   → Quantity updated

6. CREATE - User places order
   POST /api/orders { shipping_address: "..." }
   → Order created, cart cleared

7. READ - User views orders
   GET /api/orders
   → Shows order history
```

---

## SQL to CRUD Mapping

### SQL → SQLAlchemy → CRUD

| SQL | SQLAlchemy | CRUD Operation |
|-----|------------|----------------|
| `INSERT INTO products ...` | `db.session.add(product)` | CREATE |
| `SELECT * FROM products` | `Product.query.all()` | READ (all) |
| `SELECT * FROM products WHERE id=1` | `Product.query.get(1)` | READ (one) |
| `UPDATE products SET price=99.99 WHERE id=1` | `product.price = 99.99` <br> `db.session.commit()` | UPDATE |
| `DELETE FROM products WHERE id=1` | `db.session.delete(product)` <br> `db.session.commit()` | DELETE |

---

## Common Patterns

### Pattern 1: Create with Validation

```python
@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.get_json()
    
    # Validation
    if not data.get('name'):
        return jsonify({'error': 'Name required'}), 400
    
    if Product.query.filter_by(name=data['name']).first():
        return jsonify({'error': 'Product exists'}), 400
    
    # CREATE
    product = Product(**data)
    db.session.add(product)
    db.session.commit()
    
    return jsonify({'message': 'Created', 'product': {...}}), 201
```

### Pattern 2: Update Partial Fields

```python
@app.route('/api/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()
    
    # Only update provided fields
    if 'name' in data:
        product.name = data['name']
    if 'price' in data:
        product.price = data['price']
    
    db.session.commit()
    return jsonify({'message': 'Updated'}), 200
```

### Pattern 3: Delete with Cascade

```python
# When deleting a User, related CartItems are automatically deleted
# due to cascade='all, delete-orphan' in the relationship

user = User.query.get(1)
db.session.delete(user)
db.session.commit()
# All cart_items linked to this user are also deleted
```

---

## Testing CRUD with curl

### CREATE
```bash
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"name":"Test Product","price":99.99,"stock":10}'
```

### READ
```bash
curl http://localhost:5000/api/products
curl http://localhost:5000/api/products/1
```

### UPDATE
```bash
curl -X PUT http://localhost:5000/api/products/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"price":89.99}'
```

### DELETE
```bash
curl -X DELETE http://localhost:5000/api/products/1 \
  -H "Authorization: Bearer <token>"
```

---

This guide shows you exactly how CRUD operations work in this e-commerce app! 🎉

