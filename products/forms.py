from django import forms
from .models import ProductReview

class SearchForm(forms.Form):
    query = forms.CharField()

class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['rating', 'comment']
        widget = {'rating': forms.HiddenInput(),}