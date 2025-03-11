from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} → {self.name}"
        return self.name



class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey('Brand', on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    is_on_sale = models.BooleanField(default=False)
    discount_percentage = models.PositiveIntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)

    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="50" height="50"/>')
        return "No Image"
    
    image_tag.short_description = 'Image'
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('delivered', 'Delivered'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Order {self.id} - {self.product.name} ({self.status})"


class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
