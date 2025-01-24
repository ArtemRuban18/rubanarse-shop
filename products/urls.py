from django.urls import path
import products.views as views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/<slug:slug>/', views.detail_product, name='detail_product'),
    path('products/category/<slug:slug>/', views.product_category, name='product_category'),
    
]
