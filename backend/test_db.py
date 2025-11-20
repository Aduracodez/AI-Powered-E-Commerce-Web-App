"""
Quick script to check if database exists and has products
Run this from the backend directory: python test_db.py
"""

from app import app, db, Product

with app.app_context():
    # Check if database file exists
    import os
    db_path = 'ecommerce.db'
    if os.path.exists(db_path):
        print(f"✓ Database file exists: {db_path}")
    else:
        print(f"✗ Database file NOT found: {db_path}")
        print("  → Need to run the backend server first to create the database")
        print("  → Run: python app.py")
        exit(1)
    
    # Check product count
    try:
        count = Product.query.count()
        print(f"✓ Total products in database: {count}")
        
        if count > 0:
            print("\nFirst 5 products:")
            products = Product.query.limit(5).all()
            for p in products:
                print(f"  - {p.name}: ${p.price} ({p.category})")
        else:
            print("\n✗ Database is empty!")
            print("  → Database exists but has no products")
            print("  → The seed function should have run when backend started")
            print("  → Try: Delete ecommerce.db and restart backend")
    except Exception as e:
        print(f"✗ Error querying database: {e}")
        print("  → Database might be corrupted or not initialized")
        print("  → Try: Delete ecommerce.db and restart backend")

