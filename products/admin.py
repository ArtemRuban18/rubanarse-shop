from django.contrib import admin
from .models import Product, Category, ProductReview, TypeFlavor
from .forms import ProductForm
from django.template.defaultfilters import truncatechars

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin class for Product model

    Methods:
        - get_flavor(self, obj) - returns all flavors for product
        - get_description(self, obj) - returns truncated description for product
    """

    form = ProductForm
    list_display = ['id', 'name', 'get_description','category','get_flavor','volume', 'price', 'quantity', 'available', 'views']
    search_fields = ['name', 'category', 'type_flavor', 'volume']
    list_filter = ['category', 'price', 'quantity','available', 'type_flavor']

    def get_flavor(self, obj):
        return [type_flavor.name for type_flavor in obj.type_flavor.all()]
    
    def get_description(self, obj):
        return truncatechars(obj.description, 50)
    get_description.short_description = 'Опис'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin class for Category model
    """

    list_display = ['name']

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    """
    Admin class for ProductReview model
    """

    list_display = ['user', 'product', 'comment', 'rating', 'created_at']
    search_fields = ['product', 'rating']
    list_filter = ['product', 'rating']

@admin.register(TypeFlavor)
class TypeFlavorAdmin(admin.ModelAdmin):
    """
    Admin class for TypeFlavor model
    """
    
    list_display = ['name']