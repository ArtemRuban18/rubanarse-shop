from django.contrib import admin
from .models import Cart, CartProduct

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']

@admin.register(CartProduct)
class CartProduct(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'total_price']

    def total_price(self, obj):
        return obj.product.price * obj.quantity
    
    total_price.short_description = "Загальна вартість"