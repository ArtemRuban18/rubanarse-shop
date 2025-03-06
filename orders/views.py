from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderProduct
from random import randint
from cart.models import Cart
from .forms import CreateOrderForm, EditOrderProductForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.forms import inlineformset_factory
from .tasks import send_email_confirm_order

@login_required
def create_order(request):
    """
    Views for presentation of the order creation page.
    
    Get current user`s cart.
    Check if quantity of products in cart is less than quantity products in stock.
    If form is valid, create order and redirect to detail_order page.

    Context:
        - cart: cart of current user.
        - create_order_form: form for creation new order.
        - order: created order.
    
    Templates:
        - create_order.html
    """

    cart = get_object_or_404(Cart, user=request.user)

    products_cart = cart.products.all()
    if not products_cart.exists():
        return redirect('detail_cart', username=request.user.username)
    for product_cart in products_cart:
        product = product_cart.product
        if product.quantity < product_cart.quantity:
            messages.info(request, f"Недостатня кількість товару {product.name} на складі. Максимальна можлива кількість {product.quantity}.")
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        
    order = None
    if request.method == 'POST':
        create_order_form = CreateOrderForm(request.POST)
        if create_order_form.is_valid():
            order = create_order_form.save(commit=False)
            order.user = request.user
            order.order_id = randint(1, 10000)
            order.save()
            for cart_product in cart.products.all():
                OrderProduct.objects.create(
                    order=order,
                    product=cart_product.product,
                    quantity=cart_product.quantity
                )
            return redirect('detail_order', order_id=order.order_id)
    else:
        create_order_form = CreateOrderForm()
    context = {
        'cart': cart,
        'create_order_form': create_order_form,
        'order': order
    }
    return render(request, 'create_order.html', context)

@login_required
def detail_order(request, order_id):
    """
    Views for filing order detail information.

    Get order by order_id and current user.
    Create formset for editing order products.
    If formset is valid, save order and redirect to information_about_order page.

    Context:
        - order: order by order_id and current user.
        - formset: form for editing current order.
    
    Templates:
        - detail_order.html    
    """
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    OrderProductFormSet = inlineformset_factory(Order, OrderProduct, form=EditOrderProductForm, extra=0, can_delete=True)
    
    if request.method == 'POST':
        formset = OrderProductFormSet(request.POST, instance=order)
        if formset.is_valid():
            insufficient_products = []

            for form in formset:
                if form.cleaned_data.get('DELETE'):
                    continue
                
                product = form.instance.product
                new_quantity = form.cleaned_data.get('quantity')

                if new_quantity > product.quantity:
                    insufficient_products.append(f"{product.name} (доступно: {product.quantity}, у замовленні: {new_quantity})")

            if insufficient_products:
                messages.warning(request, "Наступні товари мають недостатню кількість на складі: " + ", ".join(insufficient_products))
                return redirect('detail_order', order_id=order.order_id)

            formset.save()
            return redirect('information_about_order', order_id=order.order_id)
        else:
            context = {
                'order': order,
                'formset': formset,
            }
            return render(request, 'detail_order.html', context)
    else:
        formset = OrderProductFormSet(instance=order)
    
    context = {
        'order': order,
        'formset': formset,
    }
    return render(request, 'detail_order.html', context)

def information_about_order(request, order_id):
    """
    Views for presentation detail information about current order.

    Get order bu order_id and current user.
    
    Context:
        - order: order by order_id and current user.

    Templates:
        - information_about_order.html
    """

    order = get_object_or_404(Order, order_id=order_id, user = request.user)
    return render(request, 'information_about_order.html', {'order': order})

@login_required
@transaction.atomic
def confirm_order(request, order_id):
    """
    Views for confirmation order.

    Get order by order_id and current user.
    Check if order is confirmed.If order is confirmed, send a messga and redirect to confirm_order page.
    If order isn`t confirmed, confirm order and delete this products form cart current user and send email about confirmation order.

    Context:
        -order: order by order_id and current user.
        - total_price: rotal price thos order.
    
    Temlates:
        - confirm_order.html
    """

    order = Order.objects.prefetch_related('products__product').select_for_update().get(order_id=order_id, user=request.user)
    cart = get_object_or_404(Cart, user=request.user)
    if order.status == 'confirmed':
        messages.info(request, "Замовлення вже підтверджено.")
        return redirect('confirm_order', order_id=order.id)
        
    order.confirm_order()
    order.save()
    cart.products.all().delete()

    subject = "Підтвердження замовлення"
    message = f"{request.user.username}, Ваше замовлення підтверджено!"
    transaction.on_commit(lambda: send_email_confirm_order.delay(subject, message, [order.email], order.id))

    context ={
        'order': order,
        'total_price': order.total_price()
    }

    return render(request, 'confirm_order.html',context)