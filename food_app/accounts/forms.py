from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordResetForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import UserProfile
from django.contrib.auth.models import User

class CustomRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    delivery_address = forms.CharField(max_length=255)
    phone_number = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'delivery_address', 'phone_number', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'delivery_address', 'email', 'phone_number']







class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Your Email",
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email'}),
    )

    # You can add more fields or customize existing ones if needed

    def clean_email(self):
        email = self.cleaned_data['email']

        # Add custom email validation logic
        # For example, let's require the email to end with a specific domain
        allowed_domain = 'example.com'
        if not email.endswith(allowed_domain):
            raise ValidationError(
                _('Invalid email address. Please use an email address with the domain {}').format(allowed_domain),
                code='invalid_email',
            )

        return email



