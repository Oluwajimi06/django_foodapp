# accounts/views.py
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm  # Replace with your actual form
from django.contrib.auth.views import LoginView
# from django.core.mail import send_mail
# from django.conf import settings
# from django.urls import reverse







class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, 'Account created successfully!')


        return response


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Additional data for the template
        context["data"] = {"ptitle": "Meals order & bookings - Sign Up"}
        return context





class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Additional data for the template
        context["data"] = {"ptitle": "Meals order & bookings - Login Page"}
        return context

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        # Retrieve additional data from session
        data = request.session.pop('signup_data', {})

        # Pass the additional data to the template context
        return render(request, self.template_name, self.get_context_data(data=data))




