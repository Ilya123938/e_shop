from django import forms
class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=[(i, str(i)) for i in range(1, 21)],
        coerce=int
    )

    overwrite_quantity = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )