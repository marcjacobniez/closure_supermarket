from django import forms

class CheckoutForm(forms.Form):
    """
    Checkout
    """
    shipping_address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=True
    )
    phone = forms.CharField(max_length=15, required=True)