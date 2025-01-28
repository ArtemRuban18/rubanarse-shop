from django import forms
from .models import Order

class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'phone', 'email']
        labels = {
            'full_name':'Прізвище Ім\'я',
            'phone':'Номер телефону',
            'email':'Електрона пошта',
        }
