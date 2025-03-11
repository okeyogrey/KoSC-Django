from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Category, Product, Brand

class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'subcategories']

    def get_subcategories(self, obj):
        subcategories = Category.objects.filter(parent=obj)
        return CategorySerializer(subcategories, many=True).data
        

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name']

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all())

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'category', 'brand', 'price',
            'stock', 'is_on_sale', 'discount_percentage', 'image'
        ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])  # Ensures password is hashed securely
        user.save()
        return user
