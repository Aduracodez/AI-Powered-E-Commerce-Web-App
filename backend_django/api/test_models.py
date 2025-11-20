from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Product, CartItem, Order, OrderItem


class ProductModelTestCase(TestCase):
    """Test Product model"""
    
    def test_create_product(self):
        """Test creating a product"""
        product = Product.objects.create(
            name='Test Product',
            description='Test description',
            price=99.99,
            stock=10,
            category='Electronics'
        )
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.price, 99.99)
        self.assertEqual(product.stock, 10)
        self.assertEqual(product.category, 'Electronics')
        self.assertEqual(str(product), 'Test Product')
    
    def test_product_price_validation(self):
        """Test product price cannot be negative"""
        product = Product(
            name='Test Product',
            price=-10.0,
            stock=10
        )
        with self.assertRaises(ValidationError):
            product.full_clean()
    
    def test_product_stock_validation(self):
        """Test product stock cannot be negative"""
        product = Product(
            name='Test Product',
            price=99.99,
            stock=-5
        )
        with self.assertRaises(ValidationError):
            product.full_clean()
    
    def test_product_ordering(self):
        """Test products are ordered by created_at descending"""
        product1 = Product.objects.create(name='Product 1', price=10.0, stock=10)
        product2 = Product.objects.create(name='Product 2', price=20.0, stock=10)
        
        products = list(Product.objects.all())
        self.assertEqual(products[0].name, 'Product 2')  # Most recent first
        self.assertEqual(products[1].name, 'Product 1')


class CartItemModelTestCase(TestCase):
    """Test CartItem model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.product = Product.objects.create(
            name='Test Product',
            price=99.99,
            stock=10
        )
    
    def test_create_cart_item(self):
        """Test creating a cart item"""
        cart_item = CartItem.objects.create(
            user=self.user,
            product=self.product,
            quantity=2
        )
        self.assertEqual(cart_item.user, self.user)
        self.assertEqual(cart_item.product, self.product)
        self.assertEqual(cart_item.quantity, 2)
        self.assertEqual(str(cart_item), 'testuser - Test Product x2')
    
    def test_cart_item_unique_constraint(self):
        """Test unique constraint on user and product"""
        from django.db import IntegrityError, transaction
        
        cart_item1 = CartItem.objects.create(
            user=self.user,
            product=self.product,
            quantity=2
        )
        
        # Creating same user+product combination should raise IntegrityError
        # Use transaction.atomic to properly handle the integrity error
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                CartItem.objects.create(
                    user=self.user,
                    product=self.product,
                    quantity=3
                )
        
        # Verify first item still exists (after transaction rollback)
        self.assertEqual(CartItem.objects.count(), 1)
        cart_item1.refresh_from_db()
        self.assertEqual(cart_item1.quantity, 2)


class OrderModelTestCase(TestCase):
    """Test Order model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_create_order(self):
        """Test creating an order"""
        order = Order.objects.create(
            user=self.user,
            total_amount=199.98,
            shipping_address='123 Test St',
            status='pending'
        )
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.total_amount, 199.98)
        self.assertEqual(order.status, 'pending')
        self.assertIn('Order #', str(order))
    
    def test_create_guest_order(self):
        """Test creating a guest order"""
        order = Order.objects.create(
            user=None,
            guest_email='guest@example.com',
            guest_name='Guest User',
            total_amount=99.99,
            shipping_address='123 Test St'
        )
        self.assertIsNone(order.user)
        self.assertEqual(order.guest_email, 'guest@example.com')
        self.assertEqual(order.guest_name, 'Guest User')
        self.assertIn('Guest:', str(order))
    
    def test_order_default_status(self):
        """Test order defaults to pending status"""
        order = Order.objects.create(
            user=self.user,
            total_amount=99.99
        )
        self.assertEqual(order.status, 'pending')


class OrderItemModelTestCase(TestCase):
    """Test OrderItem model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.order = Order.objects.create(
            user=self.user,
            total_amount=199.98
        )
        self.product = Product.objects.create(
            name='Test Product',
            price=99.99,
            stock=10
        )
    
    def test_create_order_item(self):
        """Test creating an order item"""
        order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price=99.99
        )
        self.assertEqual(order_item.order, self.order)
        self.assertEqual(order_item.product, self.product)
        self.assertEqual(order_item.quantity, 2)
        self.assertEqual(order_item.price, 99.99)
        self.assertIn('Order #', str(order_item))
    
    def test_order_item_with_deleted_product(self):
        """Test order item handles deleted product"""
        order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price=99.99
        )
        product_id = self.product.id
        self.product.delete()
        
        order_item.refresh_from_db()
        self.assertIsNone(order_item.product)
        self.assertIn('Deleted Product', str(order_item))

