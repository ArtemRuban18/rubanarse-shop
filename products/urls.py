from django.urls import path
import products.views as views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/<slug:slug>/', views.detail_product, name='detail_product'),
    path('products/category/<slug:slug>/', views.product_by_category, name='product_by_category'),
    path('products/flavor/<slug:slug>/', views.product_by_flavor, name='product_by_flavor'),
    path('search/', views.search, name = 'search'),
]
