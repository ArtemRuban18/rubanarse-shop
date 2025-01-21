from django.contrib import admin
from .models import Product, Category, ProductReview
from .forms import CreateProduct

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = CreateProduct
    list_display = ['id', 'name', 'description','category','get_type_flavor','volume', 'price', 'quantity', 'available', 'views']
    search_fields = ['name', 'category', 'get_type_flavor', 'volume']
    list_filter = ['category', 'price', 'quantity','available']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ['name']

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    model = ProductReview
    list_display = ['user', 'product', 'comment', 'rating', 'created_at']
    search_fields = ['product', 'rating']
    list_filter = ['product', 'rating']