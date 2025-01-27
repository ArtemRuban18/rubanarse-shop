from django.contrib import admin
from .models import Cart, CartProduct, Like, LikeProduct

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']

@admin.register(CartProduct)
class CartProductAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'total_price']

    def total_price(self, obj):
        return obj.product.price * obj.quantity
    
    total_price.short_description = "Загальна вартість"

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']

@admin.register(LikeProduct)
class LikeProductAdmin(admin.ModelAdmin):
    list_display = ['like', 'product']
