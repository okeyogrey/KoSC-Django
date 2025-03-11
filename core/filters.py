import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='iexact')
    brand = django_filters.CharFilter(field_name='brand__name', lookup_expr='iexact')

    class Meta:
        model = Product
        fields = ['category', 'brand', 'price_min', 'price_max']
