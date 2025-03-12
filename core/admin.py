from django.contrib import admin
from .models import Category, Product, Order, Brand
from .models import Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent']
    search_fields = ['name']
    list_filter = ['parent']  # This adds a dropdown filter for main categories
    autocomplete_fields = ['parent']  # Enables a dropdown for parent selection

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'category', 'brand', 'price', 'stock',
        'is_on_sale', 'discount_percentage', 'image_tag'
    ]
    readonly_fields = ['image_tag']
    list_filter = ['category', 'brand', 'is_on_sale']
    search_fields = ['name']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'product', 'quantity', 'status', 
        'order_date', 'delivery_date'
    ]
    list_filter = ['status', 'product__category']
    search_fields = ['user__username', 'product__name']



@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['product__name', 'user__username', 'comment']
