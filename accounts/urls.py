from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .views import signup, password_reset

urlpatterns = [
    path('login/', LoginView.as_view(template_name = 'login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', signup, name='signup'),
    path('password-reset/', password_reset, name='password_reset'),
    path('password-reset-done/', PasswordResetDoneView.as_view(template_name = 'password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',PasswordResetConfirmView.as_view(template_name = 'password_resert_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete', PasswordResetCompleteView.as_view(template_name = 'password_reset_complete.html'), name='password_reset_complete'),
]