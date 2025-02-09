from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Order(models.Model):
    PAYMENT_METHOD = [
        ('upon receipt', 'При отриманні'),
        ('Full subscription', 'Повна передоплата'),
    ]

    STATUS_ORDER = [
        ('pending','в обробці'),
        ('confirmed','підтверджено'),
        ('cancelled','скасовано'),
    ]

    order_id = models.PositiveIntegerField(blank=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=False)
    phone = models.PositiveIntegerField(blank=False)
    email = models.EmailField(blank=False)
    payment_method = models.CharField(choices=PAYMENT_METHOD, default='upon receipt')
    comment = models.CharField(blank=False, default='')
    status = models.CharField(choices=STATUS_ORDER, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return sum(product.total_price() for product in self.product.all())
    
    def confirm_order(self):
        if self.status == 'pending':
            for product_order in self.products.all():
                product = product_order.product
                if product.quantity < product_order.quantity:
                    raise ValueError(f"Недостатня кількість товару {product.name} на складі.")
                product.quantity -= product_order.quantity
                product.save()
            self.status = 'confirmed'
            self.save()

    def cancel_order(self):
        if self.status != 'pending':
            raise ValueError("Замовлення вже підтверджено і не може бути скосоване!")
        for product_order in self.products.all():
            product = product_order.product
            product.quantity += product_order.quantity
            product.save()
        self.status == 'cancelled'
        self.save()
            
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