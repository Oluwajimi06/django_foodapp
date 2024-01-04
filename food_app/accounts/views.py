from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetView
from .forms import CustomPasswordResetForm
from .forms import UserProfileForm
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomRegistrationForm

def Register(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user immediately after registration
            return redirect('/')  # Redirect to your home page
    else:
        form = CustomRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})



def Login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('/')  # Redirect to your home page after login
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})



@login_required
def profile(request):
   
    return render(request, 'registration/profile.html')



@login_required
def dashboard(request):
    data={"ptitle":"Meals order & bookings - Dashboard"}
    return render(request, 'registration/dashboard.html',data)




@login_required
def editprofile(request):
    user_profile = request.user.userprofile
    

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('/profile')  # Redirect to the user's profile page
    else:
        form = UserProfileForm(instance=user_profile)
    

    return render(request, 'registration/editprofile.html', {'form': form})



@login_required
def viewprofile(request):
    user_profile = request.user.userprofile  # Assuming a one-to-one relationship between User and UserProfile
    

    return render(request, 'registration/profile.html', {'user_profile': user_profile})






class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'custom_password_reset_confirm.html'
    # Add any additional customizations if needed

# views.py


class CustomPasswordResetView(PasswordResetView):
    template_name = 'passwordreset.html'  # Use your custom template
    form_class = CustomPasswordResetForm
    # Add any additional customizations if needed








# Create your views here.
