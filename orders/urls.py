from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/',views.create_order,name='create_order'),
    path('payment/<int:order_id>/', views.order_payment, name='order_payment'),
    path('payment_success/<int:order_id>/', views.payment_success, name='payment_success'),
    path('admin/order/<int:order_id>/pdf/', views.admin_order_pdf, name='admin_order_pdf'),
]
