from django.urls import path
from .import views
from django.contrib.auth import views as auth_views
from .views import LogoutView
app_name = 'accounts'

urlpatterns=[
    path('register/',views.register,name='register'),
    path('home/',views.home,name='home'),
    path('login/',views.mylogin,name='login'),
    path('logout/',views.log_out,name='logout'),
    path('activate/<uidb64>/<token>/',views.activate,name='activate'),
    path('profile/', views.profile, name='profile'),
 
     path('password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),
     path('api/logout/', LogoutView.as_view(), name='logout'),

]