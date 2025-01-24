from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeDoneView, PasswordChangeView, PasswordResetConfirmView, PasswordResetCompleteView
from .views import signup

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logogut/', LogoutView.as_view(), name='logout'),
    path('signup/', signup, name='signup'),
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),

]