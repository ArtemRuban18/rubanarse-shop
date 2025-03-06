from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart, CartProduct
from products.models import Product
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def add_to_cart(request, product_id):
    """
    Views for adding a product to the cart of the current user.

    Get product by id and add to cart of the current user.
    Redirect to current page.
    """

    product = get_object_or_404(Product, id = product_id)
    cart, created = Cart.objects.get_or_create(user = request.user)
    cart_products, created = CartProduct.objects.get_or_create(cart = cart, product = product)
    cart_products.quantity += 1
    cart_products.save()
    next_url = request.GET.get('next', '/')
    return redirect(next_url)

@login_required
def detail_cart(request, username):
    """
    Views for presentation cart of the current user

    Get cart of the current user and display all products in the cart.
    Calculate total price of this cart.

    Context:
        - cart_products: queryset of all products in current cart.
        - cart: cart of the current user.
        - user: current user.
        : total_Price: total price of all product in the cart

    Templates:
        - detail_cart.html
    """
    user = get_object_or_404(User, username = username)

    if user != request.user:
        return redirect('detail_cart', username=request.user.username)
    
    cart, created = Cart.objects.get_or_create(user = user)
    cart_products = cart.products.all()

    total_price = sum(product.total_price() for product in cart_products)

    context = {
        'cart_products':cart_products,
        'cart':cart,
        'user':user,
        'total_price':total_price,
    }

    return render(request, 'detail_cart.html', context)

@login_required
def delete_from_cart(request, product_id):
    """
    Views for deleting product from cart of the current user.

    Get product by id and delete from cart of the current user.
    Reditect to current page.
    """
    cart = get_object_or_404(Cart, user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_product = get_object_or_404(CartProduct, cart=cart, product=product)
    cart_product.delete()
    next_url = request.GET.get('next', '/')
    return redirect(next_url)