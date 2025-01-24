from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError

class SignUp(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username':'І\'мя та прізвище',
            'email':"Електрона пошта",
            'password':'Пароль',
            'password2':'Повторіть пароль',
        }

        help_text = {
            'username':None,
            'email':None,
            'password2':None,
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget = forms.PasswordInput(attrs={"class": "form-control"})
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={"class": "form-control"})
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={"class": "form-control"})