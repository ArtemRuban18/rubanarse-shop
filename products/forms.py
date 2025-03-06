from django import forms
from .models import ProductReview,TypeFlavor,Product

class ProductForm(forms.ModelForm):
    """
    Form for creating and updating products

    Fields:
        - name: CharField
        - description: CharField
        - price: DecimalField
        - stock: IntegerField
        - image: ImageField
        - category: ModelChoiceField
        - type_flavor: ModelMultipleChoiceField
    """
    type_flavor = forms.ModelMultipleChoiceField(
        queryset=TypeFlavor.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Product
        fields = '__all__'

class SearchForm(forms.Form):
    """
    Form for searching products
    
    Fields:
        - query: CharFiled
    """
    query = forms.CharField()

class ProductReviewForm(forms.ModelForm):
    """
    Form for creating product reviews
    
    Fields:
        - rating: IntegerField
        - comment: CharField
    """
    class Meta:
        model = ProductReview
        fields = ['rating', 'comment']
        widget = {'rating': forms.HiddenInput(),}