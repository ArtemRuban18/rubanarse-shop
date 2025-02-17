from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Order

@shared_task
def send_email_confirm_order(subject, message, racipient_list, order_id):
    try:
        order = Order.objects.get(id = order_id)
        if order.status != 'cancelled':
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                racipient_list,
                fail_silently=False
            )
    except Order.DoesNotExist:
        pass