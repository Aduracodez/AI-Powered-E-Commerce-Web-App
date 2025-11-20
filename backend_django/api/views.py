from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import Product, CartItem, Order, OrderItem
from .serializers import (
    UserSerializer, UserRegistrationSerializer, CustomTokenObtainPairSerializer,
    ProductSerializer, CartItemSerializer, OrderSerializer, OrderCreateSerializer
)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            # Format response to match Flask version (frontend compatibility)
            data = response.data
            user = User.objects.get(username=request.data.get('username'))
            response.data = {
                'access_token': data['access'],  # Use access_token for frontend compatibility
                'refresh_token': data['refresh'],
                'user': UserSerializer(user).data
            }
        return response


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'User created successfully',
            'access_token': str(refresh.access_token),  # Match Flask format
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Product.objects.all()
        category = self.request.query_params.get('category', None)
        search = self.request.query_params.get('search', None)
        
        if category:
            queryset = queryset.filter(category=category)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        
        return queryset


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        
        product = get_object_or_404(Product, id=product_id)
        
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        serializer = self.get_serializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        cart_item = self.get_object()
        if cart_item.user != request.user:
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        quantity = request.data.get('quantity')
        if quantity and int(quantity) > 0:
            cart_item.quantity = int(quantity)
            cart_item.save()
            serializer = self.get_serializer(cart_item)
            return Response(serializer.data)
        
        return Response(
            {'error': 'Invalid quantity'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, *args, **kwargs):
        cart_item = self.get_object()
        if cart_item.user != request.user:
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Order.objects.filter(user=self.request.user)
        return Order.objects.none()

    def create(self, request, *args, **kwargs):
        serializer = OrderCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        
        # Handle guest order
        if not request.user.is_authenticated:
            items = data.get('items', [])
            if not items:
                return Response(
                    {'error': 'Cart is empty'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            total_amount = sum(item['price'] * item['quantity'] for item in items)
            
            order = Order.objects.create(
                user=None,
                guest_email=data.get('email', ''),
                guest_name=data.get('name', ''),
                total_amount=total_amount,
                shipping_address=data.get('shipping_address', '')
            )
            
            for item in items:
                product = Product.objects.get(id=item['product_id'])
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    price=item['price']
                )
            
            return Response({
                'message': 'Order created successfully',
                'order_id': order.id,
                'total_amount': order.total_amount
            }, status=status.HTTP_201_CREATED)
        
        # Handle authenticated user order
        cart_items = CartItem.objects.filter(user=request.user)
        
        if not cart_items.exists():
            return Response(
                {'error': 'Cart is empty'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        total_amount = sum(item.product.price * item.quantity for item in cart_items)
        
        order = Order.objects.create(
            user=request.user,
            total_amount=total_amount,
            shipping_address=data.get('shipping_address', '')
        )
        
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        
        cart_items.delete()
        
        return Response({
            'message': 'Order created successfully',
            'order_id': order.id,
            'total_amount': order.total_amount
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_guest_order(request):
    """Allow guest orders without authentication"""
    serializer = OrderCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    items = data.get('items', [])
    
    if not items:
        return Response(
            {'error': 'Cart is empty'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not data.get('email') or not data.get('name'):
        return Response(
            {'error': 'Email and name are required for guest orders'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    total_amount = sum(item['price'] * item['quantity'] for item in items)
    
    order = Order.objects.create(
        user=None,
        guest_email=data.get('email'),
        guest_name=data.get('name'),
        total_amount=total_amount,
        shipping_address=data.get('shipping_address', '')
    )
    
    for item in items:
        try:
            product = Product.objects.get(id=item['product_id'])
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['quantity'],
                price=item['price']
            )
        except Product.DoesNotExist:
            continue
    
    return Response({
        'message': 'Order created successfully',
        'order_id': order.id,
        'total_amount': order.total_amount
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def chatbot(request):
    """AI Chatbot endpoint for customer support"""
    import os
    import json
    
    user_message = request.data.get('message', '').strip()
    conversation_history = request.data.get('history', [])
    
    if not user_message:
        return Response(
            {'error': 'Message is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Get store context information
    store_context = get_store_context(request)
    
    # Try Groq API first, fallback to rule-based
    groq_api_key = os.environ.get('GROQ_API_KEY')
    
    if groq_api_key:
        try:
            response = get_groq_response(user_message, conversation_history, store_context, groq_api_key)
            return Response({'response': response})
        except Exception as e:
            print(f"Groq API error: {e}")
            # Fall through to rule-based system
    
    # Fallback to rule-based chatbot
    response = get_rule_based_response(user_message, store_context)
    return Response({'response': response})


def get_store_context(request):
    """Get relevant store information for context"""
    from .models import Product, Order
    
    # Get product categories
    categories = Product.objects.values_list('category', flat=True).distinct()
    categories = [c for c in categories if c]
    
    # Get popular products
    popular_products = Product.objects.filter(stock__gt=0)[:10]
    
    # Get user info if authenticated
    user_info = {}
    if request.user.is_authenticated:
        user_info = {
            'username': request.user.username,
            'email': request.user.email,
        }
        # Get user's recent orders
        recent_orders = Order.objects.filter(user=request.user)[:5]
        user_info['recent_orders'] = [
            {
                'id': order.id,
                'status': order.status,
                'total': order.total_amount,
                'date': order.created_at.strftime('%Y-%m-%d')
            }
            for order in recent_orders
        ]
    
    return {
        'categories': categories,
        'popular_products': [{'id': p.id, 'name': p.name, 'price': p.price} for p in popular_products],
        'user': user_info,
        'store_name': 'The Queens'
    }


def get_groq_response(message, history, context, api_key):
    """Get response from Groq API"""
    try:
        try:
            from groq import Groq
        except ImportError:
            raise Exception("Groq package not installed. Run: pip install groq==0.9.0")
        
        # Initialize Groq client with only api_key to avoid proxy issues
        # Groq client doesn't support proxies parameter
        client = Groq(api_key=api_key)
        
        # Build system prompt with store context
        system_prompt = f"""You are a helpful customer support assistant for {context['store_name']}, an e-commerce store.

Store Information:
- Product Categories: {', '.join(context['categories'])}
- Popular Products: {', '.join([p['name'] for p in context['popular_products'][:5]])}

You can help customers with:
- Product information and recommendations
- Order status and tracking
- Shipping and delivery questions
- Returns and refunds
- General store information

Keep responses friendly, concise, and helpful. If asked about specific products, suggest checking the products page.
"""
        
        # Build conversation messages
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history (last 10 messages for context)
        for msg in history[-10:]:
            messages.append({
                "role": "user" if msg.get('role') == 'user' else "assistant",
                "content": msg.get('message', '')
            })
        
        # Add current message
        messages.append({"role": "user", "content": message})
        
        # Call Groq API (using llama-3.3-70b or mixtral-8x7b-32768 for fast responses)
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",  # Fast and powerful
            temperature=0.7,
            max_tokens=200,
            top_p=1,
            stream=False
        )
        
        return chat_completion.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"Groq API error: {e}")
        raise


def get_rule_based_response(message, context):
    """Fallback rule-based chatbot responses"""
    message_lower = message.lower()
    
    # Greetings
    if any(word in message_lower for word in ['hello', 'hi', 'hey', 'greetings']):
        return f"Hello! 👋 Welcome to {context['store_name']}. How can I help you today? I can assist with product information, orders, shipping, and more!"
    
    # Product questions
    if any(word in message_lower for word in ['product', 'item', 'buy', 'purchase', 'available']):
        categories_str = ', '.join(context['categories'][:5])
        return f"We have a great selection of products! You can browse by category: {categories_str}. Would you like information about a specific product? Visit our products page to see all items."
    
    # Order questions
    if any(word in message_lower for word in ['order', 'purchase', 'status', 'tracking', 'delivery']):
        if context['user'].get('recent_orders'):
            orders_info = "\n".join([
                f"Order #{o['id']}: {o['status']} - €{o['total']:.2f} ({o['date']})"
                for o in context['user']['recent_orders'][:3]
            ])
            return f"Here are your recent orders:\n{orders_info}\n\nYou can view all orders in your Orders page."
        return "You can check your order status in the Orders section. If you have an order number, I can help you find more information!"
    
    # Shipping questions
    if any(word in message_lower for word in ['shipping', 'delivery', 'ship', 'deliver', 'when', 'how long']):
        return "We offer free shipping on all orders! Delivery typically takes 3-5 business days. You'll receive tracking information once your order ships."
    
    # Price questions
    if any(word in message_lower for word in ['price', 'cost', 'expensive', 'cheap', 'discount', 'sale']):
        return "All our prices are displayed in Euros (€). You can view product prices on the Products page. We also have regular sales and promotions - check back often for deals!"
    
    # Return/refund questions
    if any(word in message_lower for word in ['return', 'refund', 'exchange', 'cancel']):
        return "We accept returns within 30 days of purchase. Items must be in original condition. For returns or exchanges, please contact our support team with your order number."
    
    # Category questions
    if any(word in message_lower for word in ['category', 'type', 'kind', 'what do you sell']):
        categories_str = ', '.join(context['categories'])
        return f"We have products in these categories: {categories_str}. What type of product are you looking for?"
    
    # Contact/support
    if any(word in message_lower for word in ['contact', 'support', 'help', 'assistant', 'human']):
        return "I'm here to help! You can ask me about products, orders, shipping, returns, or anything else about the store. For urgent matters, please contact our support team."
    
    # Default response
    return "I'm here to help! You can ask me about:\n• Product information\n• Order status\n• Shipping and delivery\n• Returns and refunds\n• Store policies\n\nWhat would you like to know?"

