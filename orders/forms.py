from django import  forms
from .models import Order, OrderProduct
from django.forms import inlineformset_factory

class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'phone', 'email', 'comment']
        labels = {
            'full_name':'Прізвище Ім\'я',
            'phone':'Номер телефону',
            'email':'Електрона пошта',
            'comment':'Введіть адресу доставки'
        }

class EditOrderProductForm(forms.ModelForm):
    class Meta:
        model = OrderProduct
        fields = ['quantity']