from django.shortcuts import render,redirect, get_object_or_404
from .models import Order, OrderProduct
from random import randint
from cart.models import Cart
from .forms import CreateOrderForm, OrderProductFormSet
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
            return redirect('detail_order', order_id = order.id)
    else:
        create_order_form = CreateOrderForm()
    context = {
        'cart':cart,
        'create_order_form':create_order_form
    }
    return render(request, 'create_order.html', context)
        
@login_required
def detail_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == 'POST':
        formset = OrderProductFormSet(request.POST, instance=order)
        if formset.is_valid():
            formset.save()
            return redirect('confirm_order', order_id=order.id)
    else:
        formset = OrderProductFormSet(instance=order)
    
    context = {
        'order': order,
        'formset': formset,
    }
    return render(request, 'detail_order.html', context)

def confirm_order(request, order_id):
    order = get_object_or_404(Order, id = order_id)
    return render(request, 'confirm_order.html', {'order':order})