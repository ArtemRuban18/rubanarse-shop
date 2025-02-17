from django.urls import path
from django.contrib.auth import views as auth_view
from .views import signup

urlpatterns = [
    path('login/', auth_view.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/',  auth_view.LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', signup, name='signup'),
    path('password-reset/',  auth_view.PasswordResetView.as_view(
        template_name = 'password_reset.html',
        extra_email_context={
            'protocol': 'http',
            'domain': 'localhost:8000'
        }
    ), name='password_reset'),
    path('password-reset-done/',  auth_view.PasswordResetDoneView.as_view(
        template_name = 'password_reset_done.html'
    ), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',  auth_view.PasswordResetConfirmView.as_view(
        template_name = 'password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('password-reset-complete/',  auth_view.PasswordResetCompleteView.as_view(
        template_name = 'password_reset_complete.html'
    ), name='password_reset_complete'),
]