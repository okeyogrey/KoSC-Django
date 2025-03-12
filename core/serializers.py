from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Category, Product, Brand, Review
from .serializers import ReviewSerializer

class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'subcategories']

    def get_subcategories(self, obj):
        """Retrieve only direct child categories for better hierarchy control."""
        subcategories = obj.category_set.all()  # Better than querying the entire Category model
        return CategorySerializer(subcategories, many=True).data

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name']

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all())
    image = serializers.ImageField(use_url=True)  # Ensures full URL is returned
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'category', 'brand', 'price',
            'stock', 'is_on_sale', 'discount_percentage', 'image', 'reviews', 'average_rating', 'total_reviews'
        ]
    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            return round(sum([review.rating for review in reviews]) / reviews.count(), 1)
        return 0.0  # Default rating if no reviews are available

    def get_total_reviews(self, obj):
        return obj.reviews.count()



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Ensures password is write-only

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        """Ensures secure password handling with `set_password()` method."""
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']  # `create_user` securely hashes the password
        )
        return user



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'product', 'user', 'rating', 'comment', 'created_at']