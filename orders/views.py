
from django.shortcuts import render,redirect, get_object_or_404
from .models import Order, OrderProduct
from random import randint
from cart.models import Cart
from .forms import CreateOrderForm, OrderProductFormSet
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse

@login_required
def create_order(request):
    cart = get_object_or_404(Cart, user = request.user)
    products_cart = cart.products.all()
    if not products_cart.exists():
        messages.error(request, "Ваш кошик порожній. Додайте товари до кошика перед створенням замовлення.")
        return redirect('detail_cart', username=request.user.username)
    for product_cart in products_cart:
        product = product_cart.product
        if product.quantity < product_cart.quantity:
            messages.error(request, f"""Недостатня кількість товару {product.name} на складі.
                           Максимальна можлива кількість {product.quantity}""")
            return redirect('detail_cart', username = request.user.username)

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
            products_order = formset.save(commit=False)
            for product_order in products_order:
                product_order.quantity.save()
                product_order.save()
            return redirect('confirm_order', order_id=order.id)
    else:
        formset = OrderProductFormSet(instance=order)
    
    context = {
        'order': order,
        'formset': formset,
    }
    return render(request, 'detail_order.html', context)


def confirm_order(request, order_id):
    with transaction.atomic():
<<<<<<< HEAD
        order = get_object_or_404(Order.objects.select_for_update(), id=order_id, user=request.user)
        cart = get_object_or_404(Cart, user=request.user)
        if order.status == 'confirmed':
            return redirect('confirm_order', order_id=order.id)
        try:
            order.confirm_order()
            cart.products.all().delete()
        except ValueError as e:
            messages.error(request, str(e))

    return render(request, 'confirm_order.html', {'order': order})

def cancel_order(request, order_id):
    order = get_object_or_404(Order, id = order_id, user = request.user)
    try:
        order.cancel_order()
        order.delete()
        messages.success('Замовлення успішно скасовано!')
    except ValueError as e:
        messages.error(request, str(e))
    return redirect('detail_cart', order_id = order.id)
=======
        order = Order.objects.select_for_update().get(id = order_id)
        cart = get_object_or_404(Cart, user = request.user)
        if order.status == 'confirmed':
            return JsonResponse({'message':"Замовлення вже підтверджено!"})
        try:
            order.confirm_order()
            cart.products.all().delete()
            order.save()
            return JsonResponse({'message':'confirm'})
        except ValueError as e:
            return JsonResponse({'error':str(e)}, status = 400)
    context = {
        'order':order,
    }
    return render(request, 'confirm_order.html', context)
>>>>>>> 2f86da1a4fb9b380c19b191a6c4c4cd4dd535fcc
