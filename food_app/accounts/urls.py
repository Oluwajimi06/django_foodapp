from django.urls import path,include
from django.contrib.auth import views as auth_views
from .views import *
app_name="accounts"

urlpatterns = [
    path('',include('django.contrib.auth.urls')),
    path('register/',Register,name="register"),
    path('login/', Login, name='login'),
    path('accounts/profile/', profile, name='profile'),
    path('dashboard/', dashboard, name='dashboard'),
    path('editprofile/', editprofile, name='editprofile'),
    path('profile/', viewprofile, name='profile'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # Default password reset views
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
   
]

# urls.py










