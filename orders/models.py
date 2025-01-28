from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Order(models.Model):
    PAYMENT_METHOD = [
        ('upon receipt', 'При отриманні'),
        ('Full subscription', 'Повна передоплата'),
    ]

    order_id = models.PositiveIntegerField(blank=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=False)
    phone = models.PositiveIntegerField(blank=False)
    email = models.EmailField(blank=False)
    payment_method = models.CharField(choices=PAYMENT_METHOD, default='upon receipt')
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return sum(product.total_price() for product in self.product.all())
    
    def __str__(self):
        return f"{self.order_id}"
    
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='products' ,verbose_name='Замовлення')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=1, blank=True, verbose_name='Кількість')

    def total_price(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return f"{self.product} - {self.quantity}"