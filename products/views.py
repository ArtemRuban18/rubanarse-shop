from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from .models import Product, Category, TypeFlavor, ProductReview
from django.core.paginator import Paginator
from django.core.cache import cache
from .forms import SearchForm, ProductReviewForm
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
    try:
        review = ProductReview.objects.get(user = request.user, product = product)
        review_form = ProductReviewForm(request.POST or None, instance=review)
    except ProductReview.DoesNotExist:
        review_form = ProductReviewForm(request.POST or None)
    if request.method == 'POST':
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            return redirect('detail_product', slug = product.slug)
    else:
        review_form = ProductReviewForm()
    context = {
        'product':product,
        'categories':categories,
        'review_form':review_form,
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

def search(request):
    search_form = SearchForm(request.GET)
    result = []
    if search_form.is_valid():
        query = search_form.cleaned_data['query']
        result = Product.objects.filter(name__icontains = query) | Product.objects.filter(description__icontains = query)
    context = {
        'search_form':search_form,
        'result':result
    }
    return render(request, 'search.html', context)
