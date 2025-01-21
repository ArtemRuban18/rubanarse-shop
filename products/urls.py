from django.urls import path
import products.views as views

urlpatterns = [
    path('', views.index, name='index'),
]
