from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Product, CartItem, Order, OrderItem


class ProductAPITestCase(TestCase):
    """Test Product API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        
        # Create test products
        self.product1 = Product.objects.create(
            name='Test Product 1',
            description='Test description',
            price=99.99,
            stock=10,
            category='Electronics',
            image_url='https://example.com/image.jpg'
        )
        self.product2 = Product.objects.create(
            name='Test Product 2',
            description='Another test',
            price=49.99,
            stock=5,
            category='Fashion'
        )
    
    def test_list_products(self):
        """Test listing all products"""
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_list_products_pagination(self):
        """Test products pagination"""
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertEqual(response.data['count'], 2)
    
    def test_get_product_detail(self):
        """Test getting single product"""
        response = self.client.get(f'/api/products/{self.product1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Product 1')
        self.assertEqual(response.data['price'], 99.99)
    
    def test_filter_products_by_category(self):
        """Test filtering products by category"""
        response = self.client.get('/api/products/?category=Electronics')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['category'], 'Electronics')
    
    def test_search_products(self):
        """Test searching products"""
        response = self.client.get('/api/products/?search=Test Product 1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Test Product 1')
    
    def test_product_not_found(self):
        """Test product not found"""
        response = self.client.get('/api/products/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CartAPITestCase(TestCase):
    """Test Cart API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        
        # Create user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create product
        self.product = Product.objects.create(
            name='Test Product',
            price=99.99,
            stock=10
        )
        
        # Authenticate user
        self.client.force_authenticate(user=self.user)
    
    def test_add_to_cart(self):
        """Test adding product to cart"""
        response = self.client.post('/api/cart/', {
            'product_id': self.product.id,
            'quantity': 2
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CartItem.objects.count(), 1)
        self.assertEqual(CartItem.objects.first().quantity, 2)
    
    def test_add_to_cart_duplicate(self):
        """Test adding same product to cart increases quantity"""
        # Add first time
        self.client.post('/api/cart/', {
            'product_id': self.product.id,
            'quantity': 2
        })
        # Add second time
        response = self.client.post('/api/cart/', {
            'product_id': self.product.id,
            'quantity': 3
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        cart_item = CartItem.objects.first()
        self.assertEqual(cart_item.quantity, 5)  # 2 + 3
    
    def test_get_cart(self):
        """Test getting user's cart"""
        CartItem.objects.create(
            user=self.user,
            product=self.product,
            quantity=2
        )
        response = self.client.get('/api/cart/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Handle pagination format
        cart_items = response.data.get('results', response.data) if isinstance(response.data, dict) else response.data
        self.assertEqual(len(cart_items), 1)
    
    def test_update_cart_item(self):
        """Test updating cart item quantity"""
        cart_item = CartItem.objects.create(
            user=self.user,
            product=self.product,
            quantity=2
        )
        response = self.client.put(f'/api/cart/{cart_item.id}/', {
            'quantity': 5
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 5)
    
    def test_remove_from_cart(self):
        """Test removing item from cart"""
        cart_item = CartItem.objects.create(
            user=self.user,
            product=self.product,
            quantity=2
        )
        response = self.client.delete(f'/api/cart/{cart_item.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CartItem.objects.count(), 0)
    
    def test_cart_requires_authentication(self):
        """Test cart requires authentication"""
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/cart/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class OrderAPITestCase(TestCase):
    """Test Order API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        
        # Create user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create products
        self.product1 = Product.objects.create(
            name='Product 1',
            price=99.99,
            stock=10
        )
        self.product2 = Product.objects.create(
            name='Product 2',
            price=49.99,
            stock=5
        )
        
        # Add items to cart
        CartItem.objects.create(
            user=self.user,
            product=self.product1,
            quantity=2
        )
        CartItem.objects.create(
            user=self.user,
            product=self.product2,
            quantity=1
        )
        
        self.client.force_authenticate(user=self.user)
    
    def test_create_order(self):
        """Test creating an order"""
        response = self.client.post('/api/orders/', {
            'shipping_address': '123 Test St, Test City'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('order_id', response.data)
        self.assertIn('total_amount', response.data)
        
        # Verify order was created
        order = Order.objects.get(id=response.data['order_id'])
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.status, 'pending')
        
        # Verify order items
        self.assertEqual(order.items.count(), 2)
        
        # Verify cart is cleared
        self.assertEqual(CartItem.objects.count(), 0)
    
    def test_create_order_empty_cart(self):
        """Test creating order with empty cart"""
        # Clear cart
        CartItem.objects.all().delete()
        
        response = self.client.post('/api/orders/', {
            'shipping_address': '123 Test St'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_get_orders(self):
        """Test getting user's orders"""
        # Create an order
        order = Order.objects.create(
            user=self.user,
            total_amount=249.97,
            shipping_address='123 Test St'
        )
        OrderItem.objects.create(
            order=order,
            product=self.product1,
            quantity=2,
            price=99.99
        )
        
        response = self.client.get('/api/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Handle pagination format
        orders = response.data.get('results', response.data) if isinstance(response.data, dict) else response.data
        self.assertEqual(len(orders), 1)
    
    def test_guest_order(self):
        """Test creating guest order"""
        self.client.force_authenticate(user=None)
        
        response = self.client.post('/api/orders/guest/', {
            'name': 'Guest User',
            'email': 'guest@example.com',
            'shipping_address': '123 Test St',
            'items': [
                {
                    'product_id': self.product1.id,
                    'quantity': 1,
                    'price': 99.99
                }
            ]
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        order = Order.objects.get(id=response.data['order_id'])
        self.assertIsNone(order.user)
        self.assertEqual(order.guest_email, 'guest@example.com')
        self.assertEqual(order.guest_name, 'Guest User')
    
    def test_guest_order_missing_fields(self):
        """Test guest order validation"""
        self.client.force_authenticate(user=None)
        
        # Missing email
        response = self.client.post('/api/orders/guest/', {
            'name': 'Guest User',
            'shipping_address': '123 Test St',
            'items': [{'product_id': self.product1.id, 'quantity': 1, 'price': 99.99}]
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Missing items
        response = self.client.post('/api/orders/guest/', {
            'name': 'Guest User',
            'email': 'guest@example.com',
            'shipping_address': '123 Test St',
            'items': []
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AuthenticationAPITestCase(TestCase):
    """Test Authentication API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_register_user(self):
        """Test user registration"""
        response = self.client.post('/api/register/', {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'password2': 'newpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access_token', response.data)
        self.assertIn('user', response.data)
        
        # Verify user was created
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_register_password_mismatch(self):
        """Test registration with password mismatch"""
        response = self.client.post('/api/register/', {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'password2': 'differentpass'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login(self):
        """Test user login"""
        response = self.client.post('/api/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)
        self.assertIn('user', response.data)
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = self.client.post('/api/login/', {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ChatbotAPITestCase(TestCase):
    """Test Chatbot API endpoint"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        
        # Create products for context
        Product.objects.create(
            name='Test Product',
            price=99.99,
            stock=10,
            category='Electronics'
        )
    
    def test_chatbot_with_message(self):
        """Test chatbot with a message"""
        response = self.client.post('/api/chatbot/', {
            'message': 'Hello',
            'history': []
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('response', response.data)
        self.assertIsInstance(response.data['response'], str)
        self.assertGreater(len(response.data['response']), 0)
    
    def test_chatbot_empty_message(self):
        """Test chatbot with empty message"""
        response = self.client.post('/api/chatbot/', {
            'message': '',
            'history': []
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    def test_chatbot_no_message(self):
        """Test chatbot without message"""
        response = self.client.post('/api/chatbot/', {
            'history': []
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_chatbot_with_history(self):
        """Test chatbot with conversation history"""
        response = self.client.post('/api/chatbot/', {
            'message': 'What products do you have?',
            'history': [
                {'role': 'user', 'message': 'Hello'},
                {'role': 'assistant', 'message': 'Hi there!'}
            ]
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('response', response.data)
    
    def test_chatbot_product_question(self):
        """Test chatbot with product-related question"""
        response = self.client.post('/api/chatbot/', {
            'message': 'What products do you sell?',
            'history': []
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should mention products or categories
        self.assertIn('response', response.data)
        response_text = response.data['response'].lower()
        self.assertTrue(
            'product' in response_text or 
            'electronics' in response_text or
            'category' in response_text
        )


class ModelTestCase(TestCase):
    """Test Models"""
    
    def test_product_creation(self):
        """Test product model creation"""
        product = Product.objects.create(
            name='Test Product',
            description='Test description',
            price=99.99,
            stock=10,
            category='Electronics'
        )
        self.assertEqual(str(product), 'Test Product')
        self.assertEqual(product.price, 99.99)
        self.assertEqual(product.stock, 10)
    
    def test_cart_item_creation(self):
        """Test cart item model creation"""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        product = Product.objects.create(
            name='Test Product',
            price=99.99,
            stock=10
        )
        cart_item = CartItem.objects.create(
            user=user,
            product=product,
            quantity=2
        )
        self.assertEqual(str(cart_item), 'testuser - Test Product x2')
    
    def test_order_creation(self):
        """Test order model creation"""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        order = Order.objects.create(
            user=user,
            total_amount=199.98,
            shipping_address='123 Test St'
        )
        self.assertIn('Order #', str(order))
        self.assertEqual(order.status, 'pending')
    
    def test_guest_order_creation(self):
        """Test guest order model creation"""
        order = Order.objects.create(
            user=None,
            guest_email='guest@example.com',
            guest_name='Guest User',
            total_amount=99.99,
            shipping_address='123 Test St'
        )
        self.assertIn('Guest:', str(order))
        self.assertEqual(order.guest_email, 'guest@example.com')

