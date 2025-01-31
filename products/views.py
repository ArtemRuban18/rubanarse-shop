from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from .models import Product, Category, ProductReview, TypeFlavor
from django.core.paginator import Paginator
from django.core.cache import cache
from .forms import SearchForm
from .filters import ProductFilter

def home(request):
    products = cache.get('product_list')
    if not products:
        products = Product.objects.all()
        cache.set('product_list', products, timeout = 60*10)
    filter = ProductFilter(request.GET, queryset=products)
    categories = Category.objects.all()
    paginator = Paginator(products, 25)
    page_number = request.GET.get('page')
    page_products = paginator.get_page(page_number)
    context = {
        'products':products,
        'categories':categories,
        'page_products':page_products,
        'filter':filter,

    }
    return render(request, "home.html", context)

def detail_product(request, slug):
    product = get_object_or_404(Product, slug = slug)
    product.views += 1
    product.save()
    categories = Category.objects.all()
    context = {
        'product':product,
        'categories':categories
    }
    return render(request,"detail_product.html", context)

def product_category(request, slug):
    category = get_list_or_404(Category, slug = slug)
    products = cache.get('product_category')
    if not products:
        products = Product.objects.filter(category = category)
        cache.set(products, 'product_category', timeout=60*20)
    categories = Category.objects.all()
    paginator = Paginator(products, 25)
    page_number = request.GET.get('page')
    page_products = paginator.get_page(page_number)
    context = {
        'category':category,
        'categories':categories,
        'products':products,
        'page_products':page_products,
    }
    return render(request,"product_category.html", context)

