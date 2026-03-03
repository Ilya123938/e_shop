from .models import Account
from django import forms
from django.utils.translation import gettext_lazy as _

class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={
            'placeholder': _('Enter your password'),
            'class': 'form-control'
        })
    )
    confirm_password = forms.CharField(
        label=_("Confirm Password"),
        widget=forms.PasswordInput(attrs={
            'placeholder': _('Confirm your password'),
            'class': 'form-control'
        })
    )

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'country']

        labels = {
            'username': _('Username'),
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
            'email': _('Email'),
            'phone_number': _('Phone Number'),
            'country': _('Country'),
        }

        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': _('Enter your username'),
                'class': 'form-control'
            }),
            'first_name': forms.TextInput(attrs={
                'placeholder': _('Enter your first name'),
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': _('Enter your last name'),
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': _('Enter your email'),
                'class': 'form-control'
            }),
            'phone_number': forms.TextInput(attrs={
                'placeholder': _('Enter your phone number'),
                'class': 'form-control'
            }),
            'country': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

    def clean(self):
        clean_data = super().clean()
        password = clean_data.get('password')
        confirm_password = clean_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError(
                _('Your confirm password does not match')
            )
        return clean_data


class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['username', 'first_name', 'last_name', 'email', 'country']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Enter your username')}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Enter your first name')}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Enter your last name')}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Enter your email')}),
            'country': forms.Select(attrs={'class': 'form-control'}),
        }