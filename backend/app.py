from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///ecommerce.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

CORS(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    cart_items = db.relationship('CartItem', backref='user', lazy=True, cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='user', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(500))
    stock = db.Column(db.Integer, default=0)
    category = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    cart_items = db.relationship('CartItem', backref='product', lazy=True)
    order_items = db.relationship('OrderItem', backref='product', lazy=True)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    guest_email = db.Column(db.String(120))
    guest_name = db.Column(db.String(200))
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='pending')
    shipping_address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

# Routes
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(username=data['username'], email=data['email'], password=hashed_password)
    db.session.add(user)
    db.session.commit()
    
    access_token = create_access_token(identity=user.id)
    return jsonify({
        'message': 'User created successfully',
        'access_token': access_token,
        'user': {'id': user.id, 'username': user.username, 'email': user.email}
    }), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({
            'access_token': access_token,
            'user': {'id': user.id, 'username': user.username, 'email': user.email}
        }), 200
    
    return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/api/products', methods=['GET'])
def get_products():
    category = request.args.get('category')
    search = request.args.get('search')
    
    query = Product.query
    
    if category:
        query = query.filter_by(category=category)
    if search:
        query = query.filter(Product.name.contains(search) | Product.description.contains(search))
    
    products = query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'description': p.description,
        'price': p.price,
        'image_url': p.image_url,
        'stock': p.stock,
        'category': p.category
    } for p in products]), 200

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'image_url': product.image_url,
        'stock': product.stock,
        'category': product.category
    }), 200

@app.route('/api/cart', methods=['GET'])
@jwt_required()
def get_cart():
    user_id = get_jwt_identity()
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    
    return jsonify([{
        'id': item.id,
        'product': {
            'id': item.product.id,
            'name': item.product.name,
            'price': item.product.price,
            'image_url': item.product.image_url,
            'stock': item.product.stock
        },
        'quantity': item.quantity
    } for item in cart_items]), 200

@app.route('/api/cart', methods=['POST'])
@jwt_required()
def add_to_cart():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    product = Product.query.get_or_404(data['product_id'])
    
    existing_item = CartItem.query.filter_by(user_id=user_id, product_id=data['product_id']).first()
    
    if existing_item:
        existing_item.quantity += data.get('quantity', 1)
    else:
        cart_item = CartItem(user_id=user_id, product_id=data['product_id'], quantity=data.get('quantity', 1))
        db.session.add(cart_item)
    
    db.session.commit()
    return jsonify({'message': 'Item added to cart'}), 201

@app.route('/api/cart/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_cart_item(item_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    
    cart_item = CartItem.query.filter_by(id=item_id, user_id=user_id).first_or_404()
    cart_item.quantity = data['quantity']
    db.session.commit()
    
    return jsonify({'message': 'Cart item updated'}), 200

@app.route('/api/cart/<int:item_id>', methods=['DELETE'])
@jwt_required()
def remove_from_cart(item_id):
    user_id = get_jwt_identity()
    cart_item = CartItem.query.filter_by(id=item_id, user_id=user_id).first_or_404()
    db.session.delete(cart_item)
    db.session.commit()
    
    return jsonify({'message': 'Item removed from cart'}), 200

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    
    # Check if user is authenticated
    user_id = None
    try:
        user_id = get_jwt_identity()
    except:
        pass  # Guest order
    
    # Handle guest order
    if not user_id:
        items = data.get('items', [])
        if not items:
            return jsonify({'error': 'Cart is empty'}), 400
        
        total_amount = sum(item['price'] * item['quantity'] for item in items)
        
        order = Order(
            user_id=None,
            guest_email=data.get('email', ''),
            guest_name=data.get('name', ''),
            total_amount=total_amount,
            shipping_address=data.get('shipping_address', '')
        )
        db.session.add(order)
        db.session.flush()
        
        for item in items:
            product = Product.query.get(item['product_id'])
            if product:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item['product_id'],
                    quantity=item['quantity'],
                    price=item['price']
                )
                db.session.add(order_item)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Order created successfully',
            'order_id': order.id,
            'total_amount': order.total_amount
        }), 201
    
    # Handle authenticated user order
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    
    if not cart_items:
        return jsonify({'error': 'Cart is empty'}), 400
    
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
        db.session.delete(item)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Order created successfully',
        'order_id': order.id,
        'total_amount': order.total_amount
    }), 201

@app.route('/api/orders', methods=['GET'])
@jwt_required()
def get_orders():
    user_id = get_jwt_identity()
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
    
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
        } for item in order.items]
    } for order in orders]), 200

# Seed database with sample products
def create_tables():
    db.create_all()
    
    # Add sample products if database is empty
    if Product.query.count() == 0:
        sample_products = [
            Product(
                name='Wireless Headphones',
                description='Premium wireless headphones with noise cancellation',
                price=199.99,
                image_url='https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500',
                stock=50,
                category='Electronics'
            ),
            Product(
                name='Smart Watch',
                description='Feature-rich smartwatch with fitness tracking',
                price=299.99,
                image_url='https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500',
                stock=30,
                category='Electronics'
            ),
            Product(
                name='Running Shoes',
                description='Comfortable running shoes for all terrains',
                price=129.99,
                image_url='https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500',
                stock=100,
                category='Fashion'
            ),
            Product(
                name='Laptop Backpack',
                description='Durable laptop backpack with multiple compartments',
                price=79.99,
                image_url='https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500',
                stock=75,
                category='Accessories'
            ),
            Product(
                name='Coffee Maker',
                description='Programmable coffee maker with thermal carafe',
                price=149.99,
                image_url='https://images.unsplash.com/photo-1517668808823-b8920ac547e8?w=500',
                stock=40,
                category='Home'
            ),
            Product(
                name='Yoga Mat',
                description='Non-slip yoga mat for all fitness levels',
                price=39.99,
                image_url='https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=500',
                stock=120,
                category='Fitness'
            ),
            Product(
                name='Gaming Laptop',
                description='High-performance gaming laptop with RTX graphics',
                price=1299.99,
                image_url='https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=500',
                stock=25,
                category='Electronics'
            ),
            Product(
                name='Wireless Mouse',
                description='Ergonomic wireless mouse with precision tracking',
                price=49.99,
                image_url='https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=500',
                stock=200,
                category='Electronics'
            ),
            Product(
                name='Mechanical Keyboard',
                description='RGB mechanical keyboard with Cherry MX switches',
                price=129.99,
                image_url='https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=500',
                stock=80,
                category='Electronics'
            ),
            Product(
                name='Designer Sunglasses',
                description='UV protection sunglasses with polarized lenses',
                price=149.99,
                image_url='https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=500',
                stock=90,
                category='Fashion'
            ),
            Product(
                name='Leather Jacket',
                description='Premium genuine leather jacket',
                price=299.99,
                image_url='https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500',
                stock=40,
                category='Fashion'
            ),
            Product(
                name='Casual Sneakers',
                description='Comfortable everyday sneakers',
                price=79.99,
                image_url='https://images.unsplash.com/photo-1549298916-b41d501d3772?w=500',
                stock=150,
                category='Fashion'
            ),
            Product(
                name='Smartphone',
                description='Latest model smartphone with advanced camera',
                price=799.99,
                image_url='https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=500',
                stock=60,
                category='Electronics'
            ),
            Product(
                name='Tablet',
                description='10-inch tablet perfect for work and entertainment',
                price=449.99,
                image_url='https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=500',
                stock=45,
                category='Electronics'
            ),
            Product(
                name='Bluetooth Speaker',
                description='Portable Bluetooth speaker with 360° sound',
                price=89.99,
                image_url='https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=500',
                stock=100,
                category='Electronics'
            ),
            Product(
                name='Standing Desk',
                description='Adjustable height standing desk',
                price=399.99,
                image_url='https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=500',
                stock=30,
                category='Home'
            ),
            Product(
                name='Desk Chair',
                description='Ergonomic office chair with lumbar support',
                price=249.99,
                image_url='https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=500',
                stock=50,
                category='Home'
            ),
            Product(
                name='Bed Sheets Set',
                description='Luxury cotton bed sheets set',
                price=69.99,
                image_url='https://images.unsplash.com/photo-1586444248902-2f64eddc13df?w=500',
                stock=120,
                category='Home'
            ),
            Product(
                name='Air Purifier',
                description='HEPA air purifier for home and office',
                price=199.99,
                image_url='https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=500',
                stock=35,
                category='Home'
            ),
            Product(
                name='Dumbbell Set',
                description='Adjustable dumbbell set 5-50 lbs',
                price=179.99,
                image_url='https://images.unsplash.com/photo-1576678927484-cc907957088c?w=500',
                stock=70,
                category='Fitness'
            ),
            Product(
                name='Resistance Bands',
                description='Set of 5 resistance bands for full body workout',
                price=29.99,
                image_url='https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=500',
                stock=200,
                category='Fitness'
            ),
            Product(
                name='Water Bottle',
                description='Insulated stainless steel water bottle',
                price=24.99,
                image_url='https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500',
                stock=300,
                category='Accessories'
            ),
            Product(
                name='Phone Case',
                description='Protective phone case with card holder',
                price=19.99,
                image_url='https://images.unsplash.com/photo-1606889641837-6a1ee95b5323?w=500',
                stock=500,
                category='Accessories'
            ),
            Product(
                name='Laptop Stand',
                description='Adjustable aluminum laptop stand',
                price=39.99,
                image_url='https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=500',
                stock=150,
                category='Accessories'
            ),
            Product(
                name='Wireless Charger',
                description='Fast wireless charging pad',
                price=34.99,
                image_url='https://images.unsplash.com/photo-1580910051074-3eb694886505?w=500',
                stock=180,
                category='Accessories'
            ),
            Product(
                name='Gaming Monitor',
                description='27-inch 4K gaming monitor with 144Hz refresh rate',
                price=449.99,
                image_url='https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=500',
                stock=35,
                category='Electronics'
            ),
            Product(
                name='Webcam HD',
                description='1080p HD webcam for video conferencing',
                price=79.99,
                image_url='https://images.unsplash.com/photo-1587825140708-dfaf72ae4b04?w=500',
                stock=150,
                category='Electronics'
            ),
            Product(
                name='USB-C Hub',
                description='Multi-port USB-C hub with HDMI and SD card reader',
                price=49.99,
                image_url='https://images.unsplash.com/photo-1625842268584-8f3296236761?w=500',
                stock=200,
                category='Accessories'
            ),
            Product(
                name='External SSD',
                description='1TB portable external SSD with fast transfer speeds',
                price=129.99,
                image_url='https://images.unsplash.com/photo-1587854692152-cbe660dbde88?w=500',
                stock=80,
                category='Electronics'
            ),
            Product(
                name='Noise Cancelling Earbuds',
                description='Premium true wireless earbuds with active noise cancellation',
                price=179.99,
                image_url='https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=500',
                stock=120,
                category='Electronics'
            ),
            Product(
                name='Smart TV 55"',
                description='55-inch 4K UHD Smart TV with streaming apps',
                price=599.99,
                image_url='https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=500',
                stock=20,
                category='Electronics'
            ),
            Product(
                name='Gaming Console',
                description='Latest generation gaming console with 1TB storage',
                price=499.99,
                image_url='https://images.unsplash.com/photo-1606813907291-d86efa9b94db?w=500',
                stock=45,
                category='Electronics'
            ),
            Product(
                name='Denim Jeans',
                description='Classic fit denim jeans in multiple washes',
                price=89.99,
                image_url='https://images.unsplash.com/photo-1542272604-787c3835535d?w=500',
                stock=200,
                category='Fashion'
            ),
            Product(
                name='Winter Coat',
                description='Warm insulated winter coat with hood',
                price=159.99,
                image_url='https://images.unsplash.com/photo-1539533018447-63fcce2678e3?w=500',
                stock=75,
                category='Fashion'
            ),
            Product(
                name='Designer Handbag',
                description='Elegant leather handbag with multiple compartments',
                price=249.99,
                image_url='https://images.unsplash.com/photo-1590874103328-eac38a683ce7?w=500',
                stock=60,
                category='Fashion'
            ),
            Product(
                name='Classic Watch',
                description='Timeless stainless steel watch with leather strap',
                price=199.99,
                image_url='https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500',
                stock=100,
                category='Fashion'
            ),
            Product(
                name='Memory Foam Mattress',
                description='Queen size memory foam mattress for better sleep',
                price=599.99,
                image_url='https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=500',
                stock=30,
                category='Home'
            ),
            Product(
                name='Smart Thermostat',
                description='Wi-Fi enabled smart thermostat with app control',
                price=249.99,
                image_url='https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=500',
                stock=50,
                category='Home'
            ),
            Product(
                name='Robot Vacuum',
                description='Smart robot vacuum with app control and scheduling',
                price=349.99,
                image_url='https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=500',
                stock=40,
                category='Home'
            ),
            Product(
                name='Kitchen Mixer',
                description='Stand mixer with multiple attachments',
                price=399.99,
                image_url='https://images.unsplash.com/photo-1578849278619-e73505e9610f?w=500',
                stock=25,
                category='Home'
            ),
            Product(
                name='Dining Table Set',
                description='6-piece dining table set with chairs',
                price=799.99,
                image_url='https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=500',
                stock=15,
                category='Home'
            ),
            Product(
                name='Treadmill',
                description='Foldable treadmill with incline and programs',
                price=899.99,
                image_url='https://images.unsplash.com/photo-1576678927484-cc907957088c?w=500',
                stock=20,
                category='Fitness'
            ),
            Product(
                name='Adjustable Bench',
                description='Home gym adjustable weight bench',
                price=199.99,
                image_url='https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=500',
                stock=40,
                category='Fitness'
            ),
            Product(
                name='Kettlebell Set',
                description='Set of 3 kettlebells (10lb, 20lb, 30lb)',
                price=89.99,
                image_url='https://images.unsplash.com/photo-1576678927484-cc907957088c?w=500',
                stock=60,
                category='Fitness'
            ),
            Product(
                name='Foam Roller',
                description='High-density foam roller for muscle recovery',
                price=24.99,
                image_url='https://images.unsplash.com/photo-1549060279-7e168fcee0c2?w=500',
                stock=150,
                category='Fitness'
            ),
            Product(
                name='Smart Scale',
                description='Body composition scale with app connectivity',
                price=79.99,
                image_url='https://images.unsplash.com/photo-1596178065887-1198b6148b2b?w=500',
                stock=80,
                category='Fitness'
            ),
            Product(
                name='Laptop Sleeve',
                description='Protective neoprene laptop sleeve',
                price=29.99,
                image_url='https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500',
                stock=250,
                category='Accessories'
            ),
            Product(
                name='Power Bank',
                description='20000mAh portable power bank with fast charging',
                price=39.99,
                image_url='https://images.unsplash.com/photo-1609091839311-d5365f9ff1c7?w=500',
                stock=300,
                category='Accessories'
            ),
            Product(
                name='Cable Organizer',
                description='Cable management system for desk',
                price=14.99,
                image_url='https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=500',
                stock=400,
                category='Accessories'
            ),
            Product(
                name='Screen Protector',
                description='Tempered glass screen protector for smartphones',
                price=12.99,
                image_url='https://images.unsplash.com/photo-1606889641837-6a1ee95b5323?w=500',
                stock=500,
                category='Accessories'
            )
        ]
        db.session.add_all(sample_products)
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        create_tables()
    
    app.run(debug=True, port=5000)

