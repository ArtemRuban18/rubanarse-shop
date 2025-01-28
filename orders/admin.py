from django.contrib import admin
from .models import Order, OrderProduct

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id','full_name','phone', 'email', 'created_at']
    ordering = ['created_at']
    list_filter = ['order_id', 'email', 'full_name']
    search_fields = ['full_name', 'email', 'order_id']

@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'total_price']
    search_fields = ['order__order_id']

    def total_price(self, obj):
        return obj.product.price * obj.quantity
    
    total_price.short_description = "Загальна Сума"
