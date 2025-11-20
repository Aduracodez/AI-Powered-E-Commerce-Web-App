from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    register, CustomTokenObtainPairView, ProductViewSet, 
    CartItemViewSet, OrderViewSet, create_guest_order, chatbot
)

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'cart', CartItemViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('orders/guest/', create_guest_order, name='guest_order'),
    path('chatbot/', chatbot, name='chatbot'),
    path('', include(router.urls)),
]

