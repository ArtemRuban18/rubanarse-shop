from shop.celery import app
from cart.models import Cart
from django.contrib.auth.models import User

@app.task(bind=True)
def create_cart(self, user_id):
    user = User.objects.get(id = user_id)
    cart, created  = Cart.objects.get_or_create(user = user)
    return cart.id