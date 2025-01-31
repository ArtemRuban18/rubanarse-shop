from django import  forms
from .models import Order, OrderProduct
from django.forms import inlineformset_factory

class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'phone', 'email']
        labels = {
            'full_name':'Прізвище Ім\'я',
            'phone':'Номер телефону',
            'email':'Електрона пошта',
        }

class EditOrderProductForm(forms.ModelForm):
    class Meta:
        model = OrderProduct
        fields = ['product', 'quantity']
        widgets = {
            'product': forms.TextInput(attrs={'readonly': 'readonly'})  
        }

OrderProductFormSet = inlineformset_factory(
    Order, 
    OrderProduct, 
    form=EditOrderProductForm,  
    fields=['product', 'quantity'],  
    extra=0,  
)