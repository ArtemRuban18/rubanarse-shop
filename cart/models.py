from django.db import models
from products.models import Product
from django.contrib.auth.models import User

class Cart(models.Model):
    """
    Model for cart of users

    Fields:
        -user: Foreign key to User Model
        - created_at: creation date(DateTimeField)
    """
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Користувач')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')

    def total_price(self):
        return sum(product.total_price() for product in self.products.all())

    def __str__(self):
        return f"Кошик {self.user}"

class CartProduct(models.Model):
    """
    Model for products in cart
    
    Fields:
        - cart: cart o user(Foreign Key)
        - product: product in cart(Foreign Key)
        - quantity: quantity of product in cart(PositiveIntegerField)
    """

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='products',  verbose_name='Кошик')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,  verbose_name='Назва товару')
    quantity = models.PositiveIntegerField(blank=True,  verbose_name='Кількість', default = 0)

    def total_price(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return f"Додано {self.product} - {self.quantity}"