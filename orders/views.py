from django.shortcuts import render,redirect, get_object_or_404
from .models import Order, OrderProduct
from random import randint
from cart.models import Cart
from .forms import CreateOrderForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User

@login_required
def create_order(request):
    cart = get_object_or_404(Cart, user = request.user)
    if request.method == 'POST':
        create_order_form = CreateOrderForm(request.POST)
        if create_order_form.is_valid():
            order = create_order_form.save(commit=False)
            order.user = request.user
            order.order_id = randint(1, 10000)
            order.save()
            for cart_product in cart.products.all():
                OrderProduct.objects.create(
                    order = order,
                    product = cart_product.product,
                    quantity = cart_product.quantity
                )
            return redirect('order_detail', order_id = order.id)
    else:
        create_order_form = CreateOrderForm()
    context = {
        'cart':cart,
        'create_order_form':create_order_form
    }
    return render(request, 'create_order.html', context)
        
@login_required
def order_detail(request, order_id, username):
    user = get_object_or_404(User, username = username)
    if user != request.user:
        return HttpResponse("ERROR")
    order = get_object_or_404(Order, id = order_id, user = request.user)
    order_products = order.products.all()
    context = {
        'order':order,
        'order_products':order_products
    }
    return render(request, 'order_detail.html', context)