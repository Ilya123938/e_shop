from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from store.models import Product
from .cart import CartConfig
from .forms import CartAddProductForm
from django.contrib import messages
from coupons.forms import CouponForm

@require_POST
def cart_add(request, product_id):
    cart = CartConfig(request)
    product = get_object_or_404(Product, id=product_id, is_available=True)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, 
                 quantity=cd['quantity'],
                 overwrite_quantity=cd.get('overwrite', False))
        messages.success(request, "Product added to cart successfully.") 
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = CartConfig(request)
    product = get_object_or_404(Product, id=product_id, is_available=True)
    cart.remove(product)
    messages.success(request, "Product removed successfully.")
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = CartConfig(request)
    for item in cart: 
        item['update_quantity_form'] = CartAddProductForm(
            initial={
                'quantity': item['quantity'],
                'overwrite_quantity': True
            }
        )
    context ={
        'cart':cart,
        'coupon_form':CouponForm
    }
    return render(request,'cart_detail.html',context)


@require_POST
def cart_decrement(request, product_id):
    cart = CartConfig(request)
    product = get_object_or_404(Product, id=product_id, is_available=True)
    cart.decrement(product) 
    return redirect('cart:cart_detail')
