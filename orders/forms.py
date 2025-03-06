from django import  forms
from .models import Order, OrderProduct

class CreateOrderForm(forms.ModelForm):
    """
    Form for creating order

    Fields:
        - full_name: CharField
        - phone: CharField
        - email: EmailField
        - comment: CharField
        - payment_method: CharField
    """
    class Meta:
        model = Order
        fields = ['full_name', 'phone', 'email', 'comment','payment_method']
        labels = {
            'full_name':'Прізвище Ім\'я',
            'phone':'Номер телефону',
            'email':'Електрона пошта',
            'comment':'Введіть адресу доставки(Місто, область, відділення пошти)',
            'payment_method':'Спосіб оплати'
        }

class EditOrderProductForm(forms.ModelForm):
    """
    Form for editing order product
    
    Fields:
        - quantity
    """
    class Meta:
        model = OrderProduct
        fields = ['quantity']