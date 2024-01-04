from django.urls import path

from .views import *
app_name="sitepages"


urlpatterns = [
    path('',Home,name="homepage"),
    path('about/',About,name="aboutpage"),
    path('service/',Service,name="servicepage"),
    path('booking/',Booking,name="bookingpage"),
    path('team/',Team,name="teampage"),
    path('testimonial/',Testimonial,name="testimonialpage"),
    path('contact/',Contact,name="contactpage"),
    path('details/<int:pid>',Details,name="details"),
    path('addtocart/<int:pid>',AddtoCart,name="addtocart"),
    path('viewcart/',ViewCart,name="viewcart"),
    path('removefromcart/<int:pid>',RemovefromCart,name="addtocart"),
    path('checkout',checkout,name="checkout"),
    path('initiate_payment/<int:order_id>/<int:total_amount>/<str:email>/', initiate_payment, name='initiate_payment'),
    # path('payment_callback/', payment_callback, name='payment_callback'),
   
    # path('initiate_payment/<int:order_id>/', initiate_payment, name='initiate_payment'),
    # path('payment_callback/', payment_callback, name='payment_callback'),
    # path('order_success/', order_success_page, name='order_success_page'),
    # path('order_error/', order_error_page, name='order_error_page'),
    
    # path('paystack/callback/<int:order_id>/', paystack_callback, name='paystack_callback'),
    # path('orderhistory/', order_history, name='order_history'),
]

# Create your views here.
