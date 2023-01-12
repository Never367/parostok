from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import Order


@shared_task
def order_created(order_id):
    """
    Task to send email notification on successful order creation.
    """
    order = Order.objects.get(id=order_id)
    html_message = render_to_string('order_email.html', {
        'order_id': order_id,
        'order': order
    })
    subject = f'Оформлено замовлення №{order_id} на сайті Par.ost.ok'
    mail_sent = send_mail(subject,
                          '',
                          'Par.ost.ok',
                          [order.email],
                          html_message=html_message
                          )
    return mail_sent
