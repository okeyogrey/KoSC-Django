from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from .models import Category, Product, Brand
from .serializers import CategorySerializer, ProductSerializer, UserSerializer, BrandSerializer
from django.contrib.auth.models import User

# Category ViewSet - Shows only main categories with their subcategories
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        # Display only top-level categories in the list
        return Category.objects.filter(parent=None)

# Brand ViewSet - Includes all brands
class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

# Product ViewSet - Optimized for better performance
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category', 'brand').all()
    serializer_class = ProductSerializer

# User Registration View - Handles new user registration
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
