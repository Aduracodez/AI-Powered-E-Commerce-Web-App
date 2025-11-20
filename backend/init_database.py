#!/usr/bin/env python3
"""
Initialize the database - Creates database and seeds products
Run this script if you need to create/initialize the database manually
Usage: python init_database.py
"""

from app import app, db, Product, User, CartItem, Order, OrderItem

def init_database():
    """Create database tables and seed products"""
    with app.app_context():
        print("📦 Creating database tables...")
        db.create_all()
        print("✅ Tables created successfully")
        
        # Check if products exist
        product_count = Product.query.count()
        print(f"📊 Current products in database: {product_count}")
        
        if product_count == 0:
            print("🌱 Seeding products...")
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
                )
            ]
            
            db.session.add_all(sample_products)
            db.session.commit()
            
            final_count = Product.query.count()
            print(f"✅ Successfully seeded {final_count} products!")
            
            # Show some sample products
            print("\n📋 Sample products:")
            for product in Product.query.limit(5).all():
                print(f"   - {product.name}: ${product.price} ({product.category})")
        else:
            print(f"✅ Database already has {product_count} products")
        
        print("\n🎉 Database initialization complete!")
        print("\n📝 Next steps:")
        print("   1. Start backend: python app.py")
        print("   2. Start frontend: npm start (in frontend directory)")
        print("   3. Open browser: http://localhost:3000")

if __name__ == '__main__':
    try:
        init_database()
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        import traceback
        traceback.print_exc()

