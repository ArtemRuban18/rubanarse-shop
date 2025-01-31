from django.urls import path
from .views import create_order, detail_order, confirm_order

urlpatterns = [
    path('create-order/', create_order, name='create_order'),
    path('order/<int:order_id>/', detail_order, name='detail_order'),
    path('confirm-order/<int:order_id>/', confirm_order, name='confirm_order')
]
