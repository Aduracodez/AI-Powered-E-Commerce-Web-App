#!/bin/bash
# Quick setup script for Django backend

echo "🚀 Setting up Django E-Commerce Backend..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate

# Seed products
echo "🌱 Seeding products..."
python manage.py seed_products

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "   1. Activate virtual environment: source venv/bin/activate"
echo "   2. Create superuser (optional): python manage.py createsuperuser"
echo "   3. Start server: python manage.py runserver"
echo ""
echo "🌐 Server will run on: http://localhost:8000"
echo "📊 Admin panel: http://localhost:8000/admin/"

