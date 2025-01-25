from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeDoneView,PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .views import signup, password_change, password_reset

urlpatterns = [
    path('login/', LoginView.as_view(template_name = 'login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', signup, name='signup'),
    path('password-change/', password_change, name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/', password_reset, name='password_reset'),
    path('password-reset-done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]