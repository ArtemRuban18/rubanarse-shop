from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, TypeFlavor, ProductReview
from django.core.paginator import Paginator
from django.core.cache import cache
from .forms import SearchForm, ProductReviewForm
from .filters import ProductFilter
from django.db.models import Q
from cart.models import Cart

def home(request):
    """
    Presentation of the main page with a list of products.

    Gets a list of products from the database, filters it using ProductFilter,
    splits it into pages using Paginator and displays it on the home.html page.
    Uses caching to optimise loading speed.
    If user is authenticated, get the user`s cart and set of the products in it.Else set cart to None.

    Context:
        - Products: QuerySet of all products (can be taken from the cache).
        - page_products: Page object with the list of products for the current page (can be taken from the cache).
        - filter: A ProductFilter instance to filter the products.
        - cart_products: Set id of the products in the current user's cart.
        - cart: Current user`s cart.

    Templates:
        - home.html.

    Cache usage:
        - product_list: to store a QuerySet of all products for 10 minutes.
        - page_products_{page_number}: to store the Page object with products for a specific page for 5 minutes.
    """

    cache_key = 'product_list'
    products = cache.get(cache_key)
    if not products:
        products = Product.objects.all()
        cache.set(cache_key,products, timeout = 60*10)
    
    filter = ProductFilter(request.GET, queryset=products)

    paginator = Paginator(filter.qs, 16)
    page_number = request.GET.get('page')
    page_products = paginator.get_page(page_number)


    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        cart_products = set(cart.products.values_list('product_id', flat=True)) if cart else set()
    else:
        cart = None
        cart_products = set()

    context = {
        'products':products,
        'page_products':page_products,
        'filter':filter,
        'cart_products':cart_products,
        'cart':cart
    }
    return render(request, "home.html", context)


def detail_product(request, slug):
    """
    Presentation of the product page.

    Get a product by slug from database and increment the number of views.
    Ability to leave a comment on the product.
    Display page on the detail_product.html template.Use caching to optimise loading speed.
    If user is authenticated, get the user`s cart and set of the products in it.Else set cart to None.

    context:
        - product: detail information about product.
        - review_form: form for adding a review.
        - cart_products: set id of the products in the current user's cart.
        - product_reviews: querySet of all reviews for the product.
        - cart: current user`s cart.
    
    Templates:
        - detail_product.html
        
    Cache usege:
        -save product in cache for 5 minutes.
    """


    cache_key = f'product-{slug}'
    product = cache.get(cache_key)
    if not product:
        product = get_object_or_404(Product, slug = slug)
        cache.set(cache_key,product, timeout = 60*5)

    product.views += 1
    product.save()

    if request.method == 'POST':
        review_form = ProductReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            return redirect('detail_product', slug = product.slug)
    else:
        review_form = ProductReviewForm()
    
    product_reviews = ProductReview.objects.filter(product = product)

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        cart_products = set(cart.products.values_list('product_id', flat=True)) if cart else set()
    else:
        cart = None
        cart_products = set()

    context = {
        'product':product,
        'review_form':review_form,
        'cart_products':cart_products,
        'product_reviews':product_reviews,
        'cart':cart
    }

    return render(request,"detail_product.html", context)

def product_by_category(request, slug):
    """
    Presentation of the products by category.

    Get a category by slug from database and filter products by this category.
    Split into pages using Paginator.
    Use cache to optimize loading speed.
    If user is authenticated, get the user`s cart and set of the products in it.Else set cart to None.

    Context:
        - category: detail information about category.
        - products: queryset of all products in this category.
        - page_products: page object with the list of products for the current page.
        - filter: ProductFilter instance to filter the products
        - cart_products: set of the products in current user`s cart
        - cart: current user`s cart
    
    Templates:
        - product_category.html

    Cache usage:
        - product_category_{slug}: to store a QuerySet of all products in this category for 20 minutes.
        - product_category_{slug}_page_{page_number}: to store the Page object with products for a specific page for 5 minutes.
    """

    category = get_object_or_404(Category, slug=slug)

    cache_key = f'product_category_{slug}'
    products = cache.get(cache_key)

    if products is None: 
        products = Product.objects.select_related('category').filter(category=category)
        cache.set(cache_key, products, timeout=60 * 10)

    product_filter = ProductFilter(request.GET, queryset=products)

    paginator = Paginator(product_filter.qs, 16)
    page_number = request.GET.get('page', 1) 

    cache_page_key = f'product_category_{slug}_page_{page_number}'
    page_products = cache.get(cache_page_key)

    if page_products is None:
        page_products = paginator.get_page(page_number)
        cache.set(cache_page_key, page_products, timeout=60 * 5)

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        cart_products = set(cart.products.values_list('product_id', flat=True)) if cart else set()
    else:
        cart = None
        cart_products = set()

    context = {
        'category': category,
        'products': products,
        'page_products': page_products,
        'filter': product_filter,
        'cart_products': cart_products,
        'cart':cart
    }

    return render(request, "product_category.html", context)


def product_by_flavor(request, slug):
    """
    Presentation of the products by flavot.

    Get a flavor by slug from database and filter products by this category.
    Split into pages using Paginator.
    Use cache to optimize loading speed.
    If user is authenticated, get the user`s cart and set of the products in it.Else set cart to None.

    Context:
        - flavor: detail information about flavor.
        - products: queryset of all products in this flavor.
        - page_products: page object with the list of products for the current page.
        - filter: ProductFilter instance to filter the products
        - cart_products: set of the products in current user`s cart
        - cart: current user`s cart
    
    Templates:
        - product_flavor.html

    Cache usage:
        - product_flavor_{slug}: to store a QuerySet of all products in this category for 20 minutes.
        - product_flavor_{slug}_page_{page_number}: to store the Page object with products for a specific page for 5 minutes.
    """

    flavor = get_object_or_404(TypeFlavor, slug=slug)
    
    cache_key = f'product_flavor_{slug}'
    products = cache.get(cache_key)

    if products is None:
        products = Product.objects.filter(type_flavor=flavor).distinct()
        cache.set(cache_key, products, timeout=60 * 20)

    product_filter = ProductFilter(request.GET, queryset=products)

    paginator = Paginator(product_filter.qs, 16)
    page_number = request.GET.get('page')
    
    cache_page_key = f'product_flavor_{slug}_page_{page_number}'
    page_products = cache.get(cache_page_key)

    if page_products is None:
        page_products = paginator.get_page(page_number)
        cache.set(cache_page_key, page_products, timeout=60 * 5)

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        cart_products = set(cart.products.values_list('product_id', flat=True)) if cart else set()
    else:
        cart = None
        cart_products = set()

    context = {
        'flavor': flavor,
        'products': products,
        'page_products': page_products,
        'filter': product_filter,
        'cart_products': cart_products,
        'cart':cart
    }

    return render(request, "product_flavor.html", context)


def search(request):
    """
    Presentation of the product by search query.

    Get a search query from form and filter products by this query.
    Split into pages using Paginator.
    Use cache to optimize loading speed.

    Context:
        - search_form: for or search query.
        - result: result the search query.
        - page_products: page objext with list of products for the current page.
        - filter: productFiler instance for filter the products.
        - cart_products: set of products current user`s cart.

    Templates:
        -search.html
    """
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

    paginator = Paginator(filter.qs, 16)
    page_number = request.GET.get('page')
    page_products = paginator.get_page(page_number)
    
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        cart_products = set(cart.products.values_list('product_id', flat=True)) if cart else set()
    else:
        cart = None
        cart_products = set()

    context = {
        'search_form':search_form,
        'result':result,
        'page_products':page_products,
        'filter':filter,
        'cart_products':cart_products,
        'cart':cart
    }

    return render(request, 'search.html', context)