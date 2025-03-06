from accounts.views import *
from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core import mail

class SignUpViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('signup')
    
    def test_template_use(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'signup.html')
    
    def test_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_create_new_user(self):
        response = self.client.post(self.url, data = {
            'username':'testuser',
            'password1':'testpassword',
            'password2':'testpassword',
            'email':'some@gmail.com'
        })
        self.assertEqual(User.objects.count(), 1)
    
    def test_invalid_email(self):
        response = self.client.post(self.url, data = {
            'username':'testuser',
            'password1':'testpassword',
            'password2':'testpassword',
            'email':'some'
        })
        self.assertEqual(User.objects.count(), 0)

    def test_different_password(self):
        response = self.client.post(self.url, data = {
            'username':'testuser',
            'password1':'testpassword',
            'password2':'anotherpassword',
            'email':'some@gmail.com'
        })
        self.assertEqual(User.objects.count(), 0)

    def test_invalid_password(self):
        response = self.client.post(self.url, data = {
            'username':'testuser',
            'password1':'test',
            'password2':'test',
            'email':'some@gmail.com'
        })
        self.assertEqual(User.objects.count(), 0)
    
    def test_redirect_after_signup(self):
        response = self.client.post(self.url, data = {
            'username':'testuser',
            'password1':'testpassword',
            'password2':'testpassword',
            'email':'some@gmail.com'
        })
        self.assertRedirects(response, reverse('login'))
    
class PasswordResetViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('password_reset')
        self.user = User.objects.create_user(username='Yarmolenko', password='YarmolaTop', email='yarmola@gmail.com')
        self.client.force_login(self.user)
        
    def test_template_use(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'password_reset.html')
    
    def test_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_redirect_after_password_reset(self):
        response = self.client.post(self.url, data = {'email': 'yarmola@gmail.com'})
        self.assertRedirects(response, reverse('password_reset_done'))
    
    def test_valid_data(self):
        response = self.client.post(self.url, data = {'email': 'yarmola@gmail.com'})
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('yarmola@gmail.com', mail.outbox[0].to)
    
    def test_invalid_data(self):
        response = self.client.post(self.url, data = {'email': 'some@gmail.com'})
        self.assertEqual(len(mail.outbox), 0)

