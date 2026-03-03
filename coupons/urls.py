from django.urls import path
from .import views
app_name = 'coupons'

urlpatterns = [
    path('apply',views.coopon_aplly,name='apply')
]
