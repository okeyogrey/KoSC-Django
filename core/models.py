from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

# ------------------ CATEGORY MODEL ------------------
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)  # Added description for more details
    parent = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL,  # Prevents data loss if parent category is deleted
        null=True, 
        blank=True, 
        related_name='subcategories'
    )

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} → {self.name}"
        return self.name

# ------------------ PRODUCT MODEL ------------------
class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='products'  # Added for reverse querying
    )
    brand = models.ForeignKey(
        'Brand', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='products'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    is_on_sale = models.BooleanField(default=False)
    discount_percentage = models.PositiveIntegerField(default=0, null=True, blank=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    description = models.TextField(blank=True)

    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="50" height="50"/>')
        return "No Image"
    
    image_tag.short_description = 'Image'

    def __str__(self):
        return self.name

# ------------------ ORDER MODEL ------------------
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('delivered', 'Delivered'),
    ]

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='orders'  # Added for reverse querying
    )
    product = models.ForeignKey(
        'Product', 
        on_delete=models.CASCADE, 
        related_name='orders'
    )
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Order {self.id} - {self.product.name} ({self.status})"

# ------------------ BRAND MODEL ------------------
class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Prevents duplicate brand entries

    def __str__(self):
        return self.name



# ------------------ REVIEWS MODEL ------------------
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=1)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['product', 'user']  # Prevents duplicate reviews by the same user

    def __str__(self):
        return f"{self.product.name} - {self.user.username} ({self.rating}/5)"
