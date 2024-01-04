# forms.py
from django import forms




class CheckoutForm(forms.Form):
    full_name = forms.CharField(label='Full Name', max_length=255)
    email = forms.EmailField(label='Email')
    delivery_address = forms.CharField(label='Delivery Address', max_length=255)
    phone_number = forms.CharField(label='Phone Number', max_length=15)


