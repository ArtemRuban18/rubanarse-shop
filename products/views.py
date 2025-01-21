from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from .models import Product, Category, ProductReview
from django.core.paginator import Paginator

# Create your views here.
def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    paginator = Paginator(products, 25)
    page_number = request.GET.get('page')
    page_products = paginator.get_page(page_number)
    context = {
        'products':products,
        'categories':categories,
        'page_products':page_products,
    }
    return render(request, "home.html", context)

def detail_product(request, slug):
    product = get_object_or_404(Product, slug = slug)
    categories = Category.objects.all()
    context = {
        'product':product,
        'categories':categories
    }
    return render(request,"detail_product.html", context)

def product_category(request, slug):
    category = get_list_or_404(Category, slug = slug)
    products = Product.objects.filter(category = category)
    categories = Category.objects.all()
    paginator = Paginator(products, 25)
    page_number = request.GET.get('page')
    page_products = paginator.get_page(page_number)
    context = {
        'category':category,
        'categories':categories,
        'products':products,
        'page_products':page_products
    }
    return render(request,"product_category.html", context)
