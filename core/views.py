from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Category, Product, Brand, Review
from .serializers import (
    CategorySerializer, 
    ProductSerializer, 
    UserSerializer, 
    BrandSerializer, 
    ReviewSerializer
)
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter

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
    queryset = Product.objects.select_related('category', 'brand').prefetch_related('reviews').all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

# User Registration View - Handles new user registration
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Review ViewSet - Handles customer reviews for products
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related('product', 'user').order_by('-created_at')
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product')
        existing_review = Review.objects.filter(
            product_id=product_id, 
            user=request.user
        ).first()

        if existing_review:
            return Response(
                {"detail": "You have already reviewed this product."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)