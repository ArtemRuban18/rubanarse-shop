from django.shortcuts import render, get_object_or_404
from .models import Cart, CartProduct, Like, LikeProduct
from products.models import Product
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id = product_id)
    cart, created = Cart.objects.get_or_create(user = request.user)
    cart_products, created = CartProduct.objects.get_or_create(cart = cart, product = product)
    cart_products.quantity +=1
    cart_products.save()
    return HttpResponse(f"{product} added to cart {request.user}")

@login_required
def detail_cart(request, username):
    user = get_object_or_404(User, username = username)
    if user != request.user:
        return HttpResponse("ERROR")
    cart, created = Cart.objects.get_or_create(user = user)
    cart_products = cart.products.all()
    context = {
        'cart_products':cart_products,
        'cart':cart,
        'user':user,
    }
    return render(request, 'detail_cart.html', context)

@login_required
def delete_from_cart(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_product = get_object_or_404(CartProduct, cart=cart, product=product)
    cart_product.delete()
    return HttpResponse('delete')

@login_required
def add_to_like(request, product_id):
    product = get_object_or_404(Product, id = product_id)
    cart, created = Like.objects.get_or_create(user = request.user)
    cart_products, created = LikeProduct.objects.get_or_create(cart = cart, product = product)
    cart_products.quantity +=1
    product.likes += 1
    cart_products.save()
    return HttpResponse(f"{product} added to like {request.user}")

@login_required
def detail_like(request, username):
    user = get_object_or_404(User, username = username)
    if user != request.user:
        return HttpResponse("ERROR")
    cart, created = Like.objects.get_or_create(user = user)
    cart_products = cart.products.all()
    context = {
        'cart_products':cart_products,
        'cart':cart,
        'user':user,
    }
    return render(request, 'detail_like.html', context)

@login_required
def delete_from_like(request, product_id):
    cart = get_object_or_404(Like, user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_product = get_object_or_404(LikeProduct, cart=cart, product=product)
    cart_product.delete()
    product.likes -= 1
    product.save()
    return HttpResponse('delete')
