from django.shortcuts import render,redirect
from .forms import CouponForm
from django.views.decorators.http import require_POST
from . models import Coupon
from django.utils import timezone
# Create your views here.

@require_POST
def coopon_aplly(request):
   now = timezone.now()
   form = CouponForm(request.POST)
   if form.is_valid():
      code = form.cleaned_data['code']
      
      try:
        coupon = Coupon.objects.get(code__iexact=code,valid_for__lte=now,valid_to__gte=now,active=True)
        request.session['coupon_id'] = coupon.id
      except Coupon.DoesNotExist:
         request.session['coupon_id'] = None
    
   return redirect('cart:cart_detail')

