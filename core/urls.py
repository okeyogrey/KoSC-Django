from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, BrandViewSet

# Initialize the router for API endpoints
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'brands', BrandViewSet, basename='brand')
router.register(r'products', ProductViewSet, basename='product')

# Define the URL patterns
urlpatterns = [
    path('api/', include(router.urls)),  # Include all registered API endpoints
]
