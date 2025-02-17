from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from .models import Product, Category, TypeFlavor, ProductReview
from django.core.paginator import Paginator
from django.core.cache import cache
from .forms import SearchForm, ProductReviewForm
from .filters import ProductFilter
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def home(request):
    cache_key = 'product_list'
    products = cache.get(cache_key)
    if not products:
        products = Product.objects.all()
        cache.set(cache_key,products, timeout = 60*10)
    filter = ProductFilter(request.GET, queryset=products)
    paginator = Paginator(filter.qs, 1)
    page_number = request.GET.get('page')
    page_products = paginator.get_page(page_number)
    context = {
        'products':products,
        'page_products':page_products,
        'filter':filter,

    }
    return render(request, "home.html", context)

@login_required
def detail_product(request, slug):
    product = get_object_or_404(Product, slug = slug)
    product.views += 1
    product.save()
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
        'review_form':review_form,
    }
    return render(request,"detail_product.html", context)

def product_by_category(request, slug):
    category = get_object_or_404(Category, slug = slug)
    cache_key = f'product_category_{slug}'
    products = cache.get(cache_key)
    if not products:
        products = Product.objects.filter(category = category)
        cache.set(cache_key,products, timeout=60*20)
    filter = ProductFilter(request.GET,queryset=products)
    paginator = Paginator(filter.qs, 1)
    page_number = request.GET.get('page')
    page_products = paginator.get_page(page_number)
    context = {
        'category':category,
        'products':products,
        'page_products':page_products,
        'filter':filter
    }
    return render(request,"product_category.html", context)

def product_by_flavor(request, slug):
    flavor = get_object_or_404(TypeFlavor, slug = slug)
    cache_key = f'product_category_{slug}'
    products = cache.get(cache_key)
    if not products:
        products = Product.objects.filter(type_flavor = flavor)
        cache.set(cache_key,products, timeout=60*20)
    filter = ProductFilter(request.GET, queryset=products)
    paginator = Paginator(filter.qs, 25)
    page_number = request.GET.get('page')
    page_products = paginator.get_page(page_number)
    context = {
        'flavor':flavor,
        'products':products,
        'page_products':page_products,
        'filter':filter
    }
    return render(request,"product_flavor.html", context)

def search(request):
    search_form = SearchForm(request.GET)
    result = Product.objects.none()

    if search_form.is_valid():
        query = search_form.cleaned_data['query']
        search_result = Q(
            name__icontains = query
        ) | Q(description__icontains = query
        ) | Q(category__name__icontains = query
        ) | Q(type_flavor__name__icontains = query)
        result = Product.objects.filter(search_result).distinct()
    
    filter = ProductFilter(request.GET, queryset=result)
    paginator = Paginator(filter.qs, 25)
    page_number = request.GET.get('page')
    page_products = paginator.get_page(page_number)
        
    context = {
        'search_form':search_form,
        'result':result,
        'page_products':page_products,
        'filter':filter
    }
    return render(request, 'search.html', context)
