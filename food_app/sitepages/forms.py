# forms.py
from django import forms
from .models import UserProfile




class CheckoutForm(forms.Form):
    full_name = forms.CharField(label='Full Name', max_length=255)
    email = forms.EmailField(label='Email')
    delivery_address = forms.CharField(label='Delivery Address', max_length=255)
    phone_number = forms.CharField(label='Phone Number', max_length=15)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'delivery_address', 'email', 'phone_number']



