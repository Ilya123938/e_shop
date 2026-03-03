from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator

from .forms import RegisterForm, AccountUpdateForm
from .models import Account


def home(request):
    return render(request, 'accounts/home.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            country = form.cleaned_data['country']
            phone_number = form.cleaned_data['phone_number']
            username = email.split('@')[0]
            password = form.cleaned_data['password']

            user = Account.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                country=country,
                password=password
            )
            user.phone_number = phone_number
            user.save()

            # ارسال ايميل التفعيل
            domain_name = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': domain_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            send_email = EmailMessage(mail_subject, message, to=[email])
            send_email.send()

            login_url = reverse('accounts:login')
            return redirect(f'{login_url}?command=verification&mail={email}')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def mylogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                # استرجاع السلة من قاعدة البيانات
                request.session['cart'] = user.last_cart
                messages.success(request, 'Login successful!')
                return redirect('cart:cart_detail')
            else:
                messages.error(request, 'Your account is not activated. Please check your email.')
        else:
            messages.error(request, 'Invalid login credentials.')

        return redirect('accounts:login')

    return render(request, 'accounts/login.html')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated!')
        return redirect('accounts:login')
    else:
        messages.error(request, 'Activation link is invalid or expired.')
        return redirect('accounts:register')


@login_required(login_url='accounts:login')
def profile(request):
    if request.method == 'POST':
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been updated successfully!')
            return redirect('accounts:profile')
    else:
        form = AccountUpdateForm(instance=request.user)

    return render(request, 'accounts/profile.html', {'form': form})


@login_required(login_url='accounts:login')
def log_out(request):
    # حفظ بيانات السلة قبل تسجيل الخروج
    request.user.last_cart = request.session.get('cart', {})
    request.user.save()

    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:login')



#rest framework
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Account
from .serializers import AccountSerializer

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]


    
# account/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # هذا يحظر التوكن
            return Response({"success": True, "message": "تم تسجيل الخروج بنجاح ✅"}, status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({"success": False, "message": "لم يتم إرسال الريفريش توكن ❌"}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError:
            return Response({"success": False, "message": "التوكن غير صالح أو منتهي الصلاحية ❌"}, status=status.HTTP_400_BAD_REQUEST)



