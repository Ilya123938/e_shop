from django import forms
from .models import Order, OrderPay


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name','last_name','email','adress','postal_code','city']


class OrderPayForm(forms.ModelForm):

    class Meta:
        model = OrderPay
        fields = ['pay_phone_number','pay_image']

    # تنظيف رقم الهاتف
    def clean_pay_phone_number(self):
        pay_phone_number = self.cleaned_data.get('pay_phone_number')

        if not pay_phone_number.isdigit():
            raise forms.ValidationError('Phone number must contain only digits.')

        if len(pay_phone_number) < 10:
            raise forms.ValidationError('Phone number must be at least 10 digits long.')

        valid_prefixes = ['06','07','05']
        if not any(pay_phone_number.startswith(prefix) for prefix in valid_prefixes):
            raise forms.ValidationError('Phone number must start with 06, 07, or 05.')

        return pay_phone_number

    # تنظيف الصورة
    def clean_pay_image(self):
        pay_image = self.cleaned_data.get('pay_image')

        if pay_image:
            if not pay_image.content_type.startswith('image'):
                raise forms.ValidationError('File must be an image.')

        return pay_image