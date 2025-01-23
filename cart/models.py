from django.db import models
from products.models import Product
from django.contrib.auth.models import User

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Користувач')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')

    def total_price(self):
        return sum(product.total_price() for product in self.product.all())

    def __str__(self):
        return f"Кошик {self.user}"

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='products',  verbose_name='Кошик')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,  verbose_name='Назва товару')
    quantity = models.PositiveIntegerField(blank=False,  verbose_name='Кількість')

    def total_price(self):
        return self.product * self.quantity
    
    def __str__(self):
        return f"Додано {self.product} - {self.quantity}"
