from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'store'

urlpatterns = [
    path('',views.product_list,name='product_list'),
    path('category/<slug:slug>/', views.products_by_category, name='products_by_category'),
    path('product_search/',views.product_search,name='product_search'),
    path('product/<int:id>/',views.product_details,name='product_details'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
