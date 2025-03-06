from django.urls import path
from .views import *
urlpatterns = [
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/<str:username>/', detail_cart, name='detail_cart'),
    path('delete-product-from-cart/<int:product_id>/', delete_from_cart, name='delete_product'),
]
