from django.contrib import admin
from .models import Category, Product, Order

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price', 'stock', 'is_on_sale', 'discount_percentage']
    list_filter = ['category', 'is_on_sale']
    search_fields = ['name']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity', 'status', 'order_date', 'delivery_date']
    list_filter = ['status']
    search_fields = ['user__username', 'product__name']


