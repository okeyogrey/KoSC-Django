from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, BrandViewSet, ReviewViewSet
from . import views

# Initialize the router for API endpoints
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'brands', BrandViewSet, basename='brand')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'reviews', ReviewViewSet, basename='review')

# Correct URL patterns without the extra 'api/' prefix
urlpatterns = router.urls

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
]
