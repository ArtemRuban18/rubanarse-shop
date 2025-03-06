from accounts.forms import *
from django.test import TestCase

class SignUpFormTest(TestCase):
    def test_valid_data(self):
        form_data = {
            'username':'yarmola',
            'email':'yarmola@gmail.com',
            'password1':'dynamokyiv123',
            'password2':'dynamokyiv123'
        }
        form = SignUp(data = form_data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_username(self):
        form_data = {
            'username':'',
            'email':'yarmola@gmail.com',
            'password1':'yarmola2345',
            'password2':'yarmola2345'
        }
        form = SignUp(data = form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username',form.errors)
    
    def test_invalid_email(self):
        form_data = {
            'username':'yarmola',
            'email':'yarmolagmail.com',
            'password1':'yarmola2345',
            'password2':'yarmola2345'
        }
        form = SignUp(data = form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_invalid_password(self):
        form_data = {
            'username':'yarmola',
            'email':'yarmola@gmail.com',
            'password1':'password12345',
            'password2':'password123456342'
        }
        form = SignUp(data = form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2',form.errors)
    
    def test_short_password(self):
        form_data = {
            'username':'yarmola',
            'email':'yarmola@gmail.com',
            'password1':'pass',
            'password2':'pass'
        }
        form = SignUp(data = form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2',form.errors)
    
    def test_empty_form_data(self):
        form_data = {}
        form = SignUp(data = form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username',form.errors)
        self.assertIn('password1',form.errors)
        self.assertIn('password2',form.errors)
    
