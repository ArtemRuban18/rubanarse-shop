from django.contrib import admin
from .models import Product, Category, ProductReview, TypeFlavor

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description','category','get_flavor','volume', 'price', 'quantity', 'available', 'views', 'likes']
    search_fields = ['name', 'category', 'type_flavor', 'volume']
    list_filter = ['category', 'price', 'quantity','available', 'type_flavor']

    def get_flavor(self, obj):
        return [type_flavor.name for type_flavor in obj.type_flavor.all()]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'comment', 'rating', 'created_at']
    search_fields = ['product', 'rating']
    list_filter = ['product', 'rating']

@admin.register(TypeFlavor)
class TypeFlavorAdmin(admin.ModelAdmin):
    list_display = ['name']