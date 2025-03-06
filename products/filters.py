import django_filters
from .models import Product, Category, TypeFlavor

class ProductFilter(django_filters.FilterSet):
    """
    Filter for products

    Fields:
        - name: CharField
        - price__lte: NumberField
        - price__gte: NumberField
        - category: ModelChoiceField
        - type_flavor: ModelChoiceField
    """
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    price__lte = django_filters.NumberFilter(field_name='price', lookup_expr='lt')
    price__gte = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    category = django_filters.ModelChoiceFilter(queryset = Category.objects.all(), field_name = 'category', label = 'Категорія')
    type_flavor = django_filters.ModelChoiceFilter(queryset = TypeFlavor.objects.all(), field_name = 'type_flavor', label = 'Аромат')

    class Meta:
        model = Product
        fields = ['name', 'price__gte', 'price__lte', 'category', 'type_flavor']
