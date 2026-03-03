from celery import shared_task
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Order
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import weasyprint
from io import BytesIO

@shared_task
def send_emails(order_id) -> int:
    
        
    order = Order.objects.get(id=order_id)
    subject = f'Order Confirmation - ID: {order.order_id}'
    message = (
            f'Dear {order.first_name},\n\n'
            f'You have successfully placed an order with ID: {order.order_id}.\n'
            f'Thank you for shopping with us!\n\n'
        )
    from_email = settings.DEFAULT_FROM_EMAIL
    mail_sent = send_mail(subject, message, from_email, [order.email])
    return mail_sent

from celery import shared_task
from io import BytesIO
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
import weasyprint
from orders.models import Order

@shared_task
def payment_success_email(order_id):  # ← صححنا الاسم هنا
    order = Order.objects.get(id=order_id)
    subject = f'Payment Confirmation - Order ID: {order.order_id}'
    message = (
        f'Dear {order.first_name},\n\n'
        f'Your payment for order ID: {order.order_id} has been successfully processed.\n'
        f'Thank you for your purchase!\n\n'
    )
    from_email = settings.DEFAULT_FROM_EMAIL
    email_user = [order.email]

    html = render_to_string('orders/order_pdf.html', {'order': order})
    pdf_file = BytesIO()
    weasyprint.HTML(string=html).write_pdf(pdf_file)
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=from_email,
        to=email_user
    )
    email.attach(f'order{order.order_id}.pdf', pdf_file.getvalue(), 'application/pdf')
    email.send()