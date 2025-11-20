#!/usr/bin/env python3
"""
Reseed database with all products (including new ones)
Run this to update your database with all 50 products
Usage: python reseed_db.py
"""

from app import app, db, Product

def reseed_products():
    """Delete all products and reseed with fresh data"""
    with app.app_context():
        print("🗑️  Deleting existing products...")
        Product.query.delete()
        db.session.commit()
        print("✅ Existing products deleted")
        
        print("🌱 Adding all products...")
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
        
        count = Product.query.count()
        print(f"✅ Successfully added {count} products to database!")
        print(f"\n📦 Product breakdown:")
        from sqlalchemy import func
        categories = db.session.query(Product.category, func.count(Product.id)).group_by(Product.category).all()
        for cat, num in categories:
            print(f"   - {cat}: {num} products")
        print(f"\n🌐 Products are now available at: http://localhost:5000/api/products")
        print(f"📱 Frontend will display them automatically when you refresh the page!")

if __name__ == '__main__':
    reseed_products()

