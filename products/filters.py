import django_filters
from .models import Product, Category, TypeFlavor

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    price = django_filters.NumberFilter()
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    category = django_filters.ModelChoiceFilter(queryset = Category.objects.all(), field_name = 'category', label = 'Категорія')
    type_flavor = django_filters.ModelChoiceFilter(queryset = TypeFlavor.objects.all(), field_name = 'type_flavor', label = 'Аромат')

    class Meta:
        model = Product
        fields = ['name', 'price', 'category', 'type_flavor']
