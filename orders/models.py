from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.core.validators import MinValueValidator, MinLengthValidator


class Order(models.Model):
    """
    Model for user`s order

    Fields:
        - order_id: PositiveIntegerField
        - user: Foreign Key to User Model
        - full_name: name and surname of user(CharField)
        - phone: phone number of user(CharField)
        - email: email of user(EmailField)
        - paynet_method: method of payment(CharField)
        - comment: comment to order(CharField)
        - status: status of order(CharField)
        - created_at: creation date(DateTimeField)
    Methods:
        - total_price: return total price of order
        - confirm_order: confirm order
        - cancel_order: cancel order
    """
    
    PAYMENT_METHOD = [
        ('upon receipt', 'При отриманні'),
        ('Full subscription', 'Передоплата'),
    ]

    STATUS_ORDER = [
        ('created', 'Створено'),
        ('confirmed','підтверджено'),
        ('cancelled','скасовано'),
    ]

    order_id = models.PositiveIntegerField(blank=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=False)
    phone = models.CharField(blank=False, validators=[MinLengthValidator(10)])
    email = models.EmailField(blank=False)
    payment_method = models.CharField(choices=PAYMENT_METHOD, default='upon receipt')
    comment = models.CharField(blank=False, default='')
    status = models.CharField(choices=STATUS_ORDER, default='created')
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return sum(product.total_price() for product in self.products.all())
    
    def confirm_order(self):
        for product_order in self.products.all():
            product = product_order.product
            if product.quantity < product_order.quantity:
                raise ValueError(f"Недостатня кількість товару {product.name} на складі.")
            product.quantity -= product_order.quantity
            product.save()
        self.status = 'confirmed'
        self.save()


    def cancel_order(self):
        if self.status == 'confirmed':
            raise ValueError("Замовлення вже підтверджено і не може бути скосоване!")
        for product_order in self.products.all():
            product = product_order.product
            product.quantity += product_order.quantity
            product.save()
        self.status = 'cancelled'
        self.save()

    def __str__(self):
        return f"{self.order_id}"
    
class OrderProduct(models.Model):
    """
    Model for product in order

    Fields:
        - order: order of user(Foreign Key)
        - product: product in order(Foreign Key)
        - quantity: quantity of product in order(PositiveIntegerField)
    Methods:
        - total_price: return total price of product in order
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='products' ,verbose_name='Замовлення')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=1, blank=True, verbose_name='Кількість', validators=[MinValueValidator(1)])

    def total_price(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return f"{self.product} - {self.quantity}"