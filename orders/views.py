from django.shortcuts import render, redirect,get_object_or_404
from .models import OrderItem ,Order
from .forms import OrderCreateForm,OrderPayForm
from cart.cart import CartConfig
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from .tasks import send_emails,payment_success_email
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required
import weasyprint





from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from .tasks import send_emails



def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order_pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response)
    return response

def create_order(request):
    cart = CartConfig(request)
    success = False

    if request.method == 'POST':
        form = OrderCreateForm(request.POST, request.FILES)

        if form.is_valid():
            order = form.save()

            # حفظ منتجات الطلب
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            # حفظ نسخة من بيانات المنتجات قبل التفريغ
            cart_items = [
                {
                    'name': item['product'].name,
                    'quantity': item['quantity'],
                    'price': item['price']
                }
                for item in cart
            ]

            cart.clear()

            # إرسال البريد باستخدام Celery
            send_emails.delay(order.id)

            success = True
            return redirect('orders:order_payment', order_id=order.id)
            

        return render(
                request,
                'orders/create_order.html',
                {'order': order, 'success': success, 'cart_items': cart_items}
            )

    else:
        form = OrderCreateForm()
        messages.info(request, "Please fill in the form to create your order.")

    return render(
        request,
        'orders/create_order.html',
        {'form': form, 'cart': cart}
    )


def order_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = OrderPayForm(request.POST, request.FILES)
        if form.is_valid():
            order_pay = form.save(commit=False)
            order_pay.order = order
            order_pay.save()
            order.paid = True
            order.save()
            messages.success(request, 'Payment successful!')
            return redirect('orders:payment_success', order_id=order.id)
    else:
        form = OrderPayForm()
    return render(request, 'orders/payment_order.html', {'form': form, 'order': order})
    
def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    payment_success_email.delay(order.id)
    return render(request, 'orders/payment_success.html', {'order': order})