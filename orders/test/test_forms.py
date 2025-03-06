from orders.forms import *
from django.test import TestCase

class CreateOrderFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'full_name':'Artem',
            'phone':'**********',
            'email':'some@gmail.com',
            'comment':'something',
            'payment_method':'upon receipt'
        }

        form = CreateOrderForm(data = form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_full_name(self):
        form_data = {
            'full_name':'',
            'phone':'**********',
            'email':'some@gmail.com',
            'comment':'something',
            'payment_method':'upon receipt'
        }

        form = CreateOrderForm(data = form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('full_name', form.errors)
    
    def test_invalid_email(self):
        form_data = {
            'full_name':'Artem',
            'phone':'**********',
            'email':'something',
            'comment':'something',
            'payment_method':'upon receipt'
        }

        form = CreateOrderForm(data = form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_invalid_phone(self):
        form_data = {
            'full_name':'Artem',
            'phone':'06802378',
            'email':'some@gmail.com',
            'comment':'something',
            'payment_method':'upon receipt'
        }

        form = CreateOrderForm(data = form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)
    
    def test_invalid_comment(self):
        form_data = {
            'full_name':'Artem',
            'phone':'**********',
            'email':'some@gmail.com',
            'comment':'',
            'payment_method':'upon receipt'
        }

        form = CreateOrderForm(data = form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('comment', form.errors)

class EditOrderProductFormTest(TestCase):
    def test_valid_form(self):
        form_data = {'quantity': 5}
        form = EditOrderProductForm(data = form_data)
        
        self.assertTrue(form.is_valid())

    def test_not_positive_value(self):
        form_data = {'quantity': 0}
        form = EditOrderProductForm(data = form_data)
        
        self.assertFalse(form.is_valid())

