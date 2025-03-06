from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.conf import settings

class SignUp(UserCreationForm):
    """
    Form for user registration

    Fields:
        - username: CharField
        - email: EmailField
        - password1: CharField
        - password2: CharField
    """
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
class CustomPasswordResetForm(PasswordResetForm):
    """
    Form for password reset

    Fields:
        - email: EmailField
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget = forms.EmailInput(attrs={"autocomplete": "email"})
    
    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name=None):
        context['domain'] = settings.DEFAULT_DOMAIN
        context['protocol'] = settings.DEFAULT_PROTOCOL
        super().send_mail(subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name)