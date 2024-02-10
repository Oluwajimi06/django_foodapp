from django.shortcuts import render,redirect,get_object_or_404
from .models import FoodItem,Purchase,OrderItem,CheckoutDetails,UserProfile,Subscriber,ContactMessage
from django.db import transaction
from uuid import uuid4
import uuid 
import urllib.parse
#
from .forms import CheckoutForm,UserProfileForm

from django.contrib.auth.decorators import login_required

#
# from sitepages.forms import UserProfileForm

import hmac
import hashlib
import traceback  # Import traceback for detailed error logging
from urllib.parse import quote

from django.db.models import Max



from sitepages.models import Booking as MyAppBooking, Table as MyAppTable,BookingHistory
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
 


from decimal import Decimal
# # from paystackapi import Transaction
# from paystackapi.transaction import Transaction
# import paystack
import paystack
from django.http import JsonResponse



from datetime import datetime
from django.core.mail import send_mail,BadHeaderError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError





from django.conf import settings
import time
import random
import logging
import requests
import json
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, redirect
from django.core.mail import send_mail
from django.views.decorators.http import require_POST


logger = logging.getLogger(__name__)

# Create your views here.
def Home(request):
    if 'usercart' in request.session:
        x = request.session['usercart']
        totalnumber = len(x)
    else:
        request.session['usercart'] = []
        x = request.session['usercart']
        totalnumber = len(x)

    # Separate queries for breakfast, lunch, and dinner items
    breakfast_items = FoodItem.objects.filter(category='Breakfast')
    lunch_items = FoodItem.objects.filter(category='Lunch')
    dinner_items = FoodItem.objects.filter(category='Dinner')

    data = {
        "ptitle": "Meals order & bookings - Home page",
        "breakfast_items": breakfast_items,
        "lunch_items": lunch_items,
        "dinner_items": dinner_items,
        "ttl": totalnumber,
    }

    return render(request, "sitepages/home.html", data)


def About(request):
    data={"ptitle":"Meals order & bookings - About Us"}
    return render(request,"sitepages/about.html",data)
def Service(request):
    data={"ptitle":"Meals order & bookings - Service"}
    return render(request,"sitepages/service.html",data)
def Booking(request):
    data={"ptitle":"Meals order & bookings - Booking"}
    return render(request,"sitepages/booking.html",data)
def Team(request):
    data={"ptitle":"Meals order & bookings - Our Team"}
    return render(request,"sitepages/team.html",data)
def Testimonial(request):
    data={"ptitle":"Meals order & bookings - Testimonial"}
    return render(request,"sitepages/testimonial.html",data)
def Contact(request):
    
    if request.method == 'POST':
        message_name = request.POST['name']
        message_email = request.POST['email']
        message_subject = request.POST['subject']
        message_msg = request.POST['message']


        

        email_subject = f"{message_subject}"
        email_body = f"Sender Name: {message_name}\nSender Email: {message_email}\n\nMessage: {message_msg}"
        sender_email = message_email
        recipient_list = [settings.EMAIL_HOST_USER]

        send_mail(
            email_subject,
            email_body,
            sender_email,
            recipient_list,
            fail_silently=True
        )

         # Create an instance of ContactMessage model and save it to the database
        contact_message = ContactMessage.objects.create(
            name=message_name,
            email=message_email,
            subject=message_subject,
            message=message_msg
        )

        

        data={"ptitle":"Meals order & bookings - Contact Us","message_name": message_name}
        return render(request,"sitepages/contact.html",data)

    else:
        data={"ptitle":"Meals order & bookings - Contact Us"}
        return render(request,"sitepages/contact.html",data)
    return render(request,"sitepages/contact.html",data)
def Details(request,pid):
    x=request.session['usercart']
    print(len(x))
    mdata = FoodItem.objects.get(id=pid)
    data={"ptitle":"Meals order & bookings - Home page","mdata": mdata}
    return render(request,"sitepages/details.html",data)


def AddtoCart(request, pid):
    x = request.session['usercart']
    x.append(pid)
    request.session['usercart'] = x
    return redirect("/viewcart")

def RemovefromCart(request, pid):
    x = request.session['usercart']
    x.remove(pid)
    request.session['usercart'] = x
    return redirect("/viewcart")

def DeletefromCart(request, pid):
    x = request.session['usercart']
    
    # Remove all occurrences of the item from the cart
    while pid in x:
        x.remove(pid)
    
    request.session['usercart'] = x
    return redirect("/viewcart")


@login_required
def profile(request):
    data={"ptitle":"Meals order & bookings - User Profile"}
    return render(request, 'registration/profile.html',data)

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
    

    return render(request, 'registration/profile.html', {'user_profile': user_profile,"ptitle":"Meals order & bookings - User Profile"})


def Subscribe(request):
    error_message = None
    success_message = None

    if request.method == 'POST':
        email = request.POST.get('email', '')

        # Perform email validation
        try:
            validate_email(email)
        except ValidationError:
            error_message = "Invalid email format. Please provide a valid email address."
        else:
            # Additional validation or processing here if needed

            # Save the email to the database (create a new Subscriber instance)
            subscriber, created = Subscriber.objects.get_or_create(email=email)

            # Custom logic for sending email when the form is valid
            subject = 'Thank you for subscribing'
            message = 'Welcome to Restoran where flavor meets delight! 🍽️ Get ready to embark on a culinary journey with us. As a valued member, you will enjoy exclusive offers, mouthwatering recipes, and delightful surprises delivered straight to your inbox. Lets savor the taste of good times together! 🎉✨'
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=True)

            success_message = f"Thank you for subscribing! An email has been sent to {email} for confirmation."

            # Redirect to subscriptionconfirm.html after successful form submission
            return render(request, 'sitepages/subscriptionconfirm.html', {'error_message': error_message, 'success_message': success_message})

    return render(request, 'sitepages/subscriptionconfirm.html', {'error_message': error_message, 'success_message': success_message})





def subscription_confirm(request):
    return render(request, 'sitepages/subscriptionconfirm.html')


@login_required
def book_table(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        datetime_str = request.POST.get('datetime')
        no_of_people = int(request.POST.get('select1'))
        message = request.POST.get('message')

        # Convert datetime string to a datetime object
        date_time_obj = datetime.strptime(datetime_str, '%m/%d/%Y %I:%M %p')

        
            # Try to get the table based on the selected type
        table =MyAppTable.objects.get(table_type=f'People {no_of_people}')

        # Get the authenticated user
        user = request.user

     
        

        # Calculate price based on the selected table type
        price = table.price
        send_confirmation_email(email,date_time_obj, no_of_people, message, price)

           # Create a Booking instance using create method
        booking = MyAppBooking.objects.create(
            user=user,
            table=table,
            booking_date=date_time_obj.date(),
            booking_time=date_time_obj.time(),
            message=message,
            payment_status='pending',  # Set initial payment status to pending
        )

        # Create a BookingHistory instance
        booking_history = BookingHistory.objects.create(
            user=user,
            booking=booking,
            payment_status='pending',  # Set initial payment status to pending
        )

        return redirect('/booking_success')

    return render(request, 'sitepages/booking.html')

def send_confirmation_email(user_email, booking_date, no_of_people, message, price):
    bank_name = "Opay Bank"
    subject = 'Booking Confirmation'
    message = f'Thank you for booking. Here are your booking details:\n\n' \
              f'Table Type: People {no_of_people}\n' \
              f'Date: {booking_date.date()}\n' \
              f'Time: {booking_date.time()}\n' \
              f'Price: {price}\n\n' \
              f'Please make a payment to the following account:\n\n' \
              f'Bank: {bank_name}\n' \
              f'Account Name: Your Restaurant\n' \
              f'Account Number: 1234567890\n' \
              f'Reference: {user_email}\n\n' \
              f'Once the payment is made, please provide the payment receipt upon arrival at the restaurant.'

    send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email], fail_silently=False)


def booking_success(request):
    data={"ptitle":"Meals order & bookings - Booking Success"}
    return render(request,'sitepages/booking_success.html',data)





@login_required
def view_booking_history(request):
    user = request.user

    # Retrieve the booking history entries for the logged-in user
    booking_history_entries = BookingHistory.objects.filter(user=user).order_by('-timestamp')

    return render(request, 'sitepages/view_booking_history.html', {'booking_history_entries': booking_history_entries,"ptitle":"Meals order & bookings - Booking History"})





def ViewCart(request):
    # Retrieve user cart from session or initialize an empty list
    x = request.session.get('usercart', [])
    y = []
    totalsum = 0
    delivery_fee = 1500

    # Loop through the unique items in the cart
    for i in set(x):
        m = FoodItem.objects.get(id=i)
        qty = x.count(i)
        unit_t = qty * int(m.price)
        totalsum += unit_t
        zee = dict(name=m.name, u_price=m.price, price=m.price, uqty=unit_t, qty=qty, pid=m.id, image=m.image.url)
        y.append(zee)

    # Store cart items in the session
    # Store cart items, totalsum, and delivery_fee in the session
    request.session['citems'] = y
    request.session['totalsum'] = totalsum
    request.session['delivery_fee'] = delivery_fee

   
    # Add delivery fee
      # Change this to your desired fixed delivery fee
    totalsum += delivery_fee  # Add the fixed delivery fee to the total

    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Check if the user has an associated profile
        try:
            user_profile = request.user.userprofile
        except UserProfile.DoesNotExist:
            user_profile = None

        # If the user has a profile, pre-fill the form with existing data
        form = UserProfileForm(instance=user_profile) if user_profile else UserProfileForm()

        return render(request, 'sitepages/viewcart.html', {'citems': y,"ptitle": "Meals order & bookings - View Cart",'tsum': totalsum, 'delivery_fee': delivery_fee, 'user_profile': user_profile, 'form': form})

    else:
        return redirect('login')
        data = {"ptitle": "Meals order & bookings - View Cart", "citems": y, "tsum": totalsum}
        return render(request, "sitepages/viewcart.html", data)



paystack_secret_key = settings.PAYSTACK_SECRET_KEY
paystack.api_key = paystack_secret_key

@login_required
def checkout(request):
    totalsum = request.session.get('totalsum', 0)
    delivery_fee = request.session.get('delivery_fee', 0)
    citems = request.session.get('citems', [])
    data = {"ptitle": "Meals order & bookings - Checkout page"}

    if request.method == 'POST':
        form = CheckoutForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                # Store checkout details in session
                request.session['delivery_address'] = form.cleaned_data['delivery_address']
                request.session['checkout_email'] = form.cleaned_data['email']
                request.session['checkout_phone_number'] = form.cleaned_data['phone_number']

                # Create a new Purchase model
                purchase = Purchase.objects.create(
                    user=request.user,
                    status='PENDING',
                    is_paid=False,  # Set is_paid to False initially
                    order_date=timezone.now(),
                    delivery_address=form.cleaned_data['delivery_address'],
                    phone_number=form.cleaned_data['phone_number'],
                    total_amount_paid=0
                )

                # Create CheckoutDetails model
                checkout_details = CheckoutDetails(
                    user=request.user,
                    full_name=form.cleaned_data['full_name'],
                    email=form.cleaned_data['email'],
                    delivery_address=form.cleaned_data['delivery_address'],
                    phone_number=form.cleaned_data['phone_number'],
                    created_at=timezone.now(),
                )
                checkout_details.save()

                # Create OrderItem models
                for item in citems:
                    OrderItem.objects.create(
                        purchase=purchase,
                        product_name=item['name'],
                        quantity=item['qty'],
                        unit_price=item['u_price'],
                        total_price=item['uqty']
                    )

                    print(f"Cart item: {item}")

                # Update total_amount_paid in Purchase
                purchase.total_amount_paid = purchase.calculate_total_amount()
                purchase.save()

                total_amount = totalsum + delivery_fee

                # Redirect to the initiate_payment page with the necessary details
                return redirect('sitepages:initiate_payment', order_id=purchase.id, total_amount=total_amount, email=form.cleaned_data['email'])
    else:
        form = CheckoutForm()

    return render(request, 'sitepages/checkout.html', {
        'form': form,
        'delivery_fee': delivery_fee,
        'totalsum': totalsum,
        'citems': citems,
        'data': data,
    })




@login_required
def order_history(request):
    # Fetch the user's paid purchases
    paid_purchases = Purchase.objects.filter(user=request.user, is_paid=True)

    return render(request, 'sitepages/order_history.html', {'purchases': paid_purchases})




# my confirm initiate_payment
paystack_secret_key = settings.PAYSTACK_SECRET_KEY  # Replace with your actual Paystack secret key

@csrf_exempt
def initiate_payment(request, order_id, total_amount, email):
    try:
        paystack_api_url = "https://api.paystack.co/transaction/initialize"

        headers = {
            "Authorization": f"Bearer {paystack_secret_key}",
            "Content-Type": "application/json",
        }

          # Generate a unique reference for the transaction
        unique_reference = str(uuid4())

       
        payload = {
            "email": email,
            "amount": int(total_amount * 100),
            "currency": "NGN",
            "reference": unique_reference,
            # Other parameters as needed
        }

        print(payload)

        response = requests.post(paystack_api_url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors

        paystack_response = response.json()
        print(paystack_response)

        # Redirect the user to Paystack payment page
        return redirect(paystack_response['data']['authorization_url'])

    except requests.exceptions.RequestException as e:
        return HttpResponse(f"Failed to initiate payment: {e}", status=500)

    except requests.exceptions.HTTPError as e:
        # Print the response content for debugging purposes
        print(f"Paystack API response content: {e.response.content}")
        return HttpResponse(f"Failed to initiate payment: {e}", status=500)

    except Exception as e:
        return HttpResponse(f"An unexpected error occurred: {e}", status=500)


 





#this webhook worked
@csrf_exempt
@require_POST
def paystack_webhook(request):
    try:
        # Replace this with your Paystack secret key
        paystack_secret_key = settings.PAYSTACK_SECRET_KEY

        # Validate the request by comparing the signature
        request_signature = request.headers.get('X-Paystack-Signature')
        paystack_signature = hmac.new(
            bytes(paystack_secret_key, 'utf-8'),
            msg=request.body,
            digestmod=hashlib.sha512
        ).hexdigest()

        if not hmac.compare_digest(request_signature, paystack_signature):
            return HttpResponse("Invalid signature", status=400)

        # Parse the webhook data
        webhook_data = json.loads(request.body.decode('utf-8'))
        event = webhook_data.get('event')

        print("Webhook Data:", webhook_data)

        if event == 'charge.success':
            # Payment was successful
            reference_from_webhook = webhook_data.get('data', {}).get('reference')

            # Retrieve the stored reference from the session
            reference_from_session = request.session.get('paystack_reference')

            # Ensure the references match
            if reference_from_webhook == reference_from_session:
                # References match, proceed with updating the Purchase model
                amount_paid = webhook_data.get('data', {}).get('amount') / 100  # Convert from kobo to naira

                # Update the Purchase model based on the reference
                try:
                    purchase = Purchase.objects.get(id=uuid.UUID(reference_from_webhook))
                    purchase.status = 'PAID'
                    purchase.total_amount_paid = amount_paid
                    purchase.save()
                except Purchase.DoesNotExist:
                    # Handle the case where the purchase does not exist
                    # You might want to log this for further investigation
                    print(f"Purchase with id {reference_from_webhook} not found.")

        return HttpResponse("Webhook received successfully", status=200)

    except Exception as e:
        return HttpResponse(f"An unexpected error occurred: {e}", status=500)



@login_required
def order_success(request):
    try:
       

        # Retrieve relevant information from the session
        citems = request.session.get('citems', [])
        delivery_address = request.session.get('delivery_address', '')
        email = request.session.get('checkout_email', '')
        phone_number = request.session.get('checkout_phone_number', '')

        # Send a confirmation email to the user
        subject = 'Order Confirmation'
        message = f'Thank you for your order!\n\nDetails:\n\n'
        for item in citems:
            message += f'{item["qty"]} x {item["name"]} - #{item["uqty"]}\n'
        message += f'\nTotal: #{request.session.get("totalsum", 0) + request.session.get("delivery_fee", 0)}'

        # Add a message before the delivery information
        message += f'\n\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx Delivery Information:\n'
        message += f'\nDelivery Address: {delivery_address}'
        message += f'\nEmail: {email}'
        message += f'\nPhone Number: {phone_number}'

        # Add a message about receiving a call from the delivery personnel
        message += f'\n\nYou will receive a call from our delivery personnel on the provided phone number.'
        
        # Add a message about the order being delivered shortly
        message += f'\n\nYour order will be delivered to you shortly. Thank you for choosing us!'

        # Send the confirmation email using email_host_user as the sender
        send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=True)

        # Clear the cart from the session
        if 'usercart' in request.session:
            del request.session['usercart']

        return render(request, 'sitepages/order_success.html')

    except BadHeaderError:
        # Handle BadHeaderError (e.g., invalid email headers) by failing silently
        pass
    except Exception as e:
        return HttpResponse(f"An unexpected error occurred: {e}", status=500)













# my confirm order_succes first
# @login_required
# def order_success(request, order_id, reference):
#     # Retrieve relevant information from the session
#     citems = request.session.get('citems', [])
#     delivery_address = request.session.get('delivery_address', '')
#     # Retrieve email from the URL
#     user_email = request.GET.get('email', '')

#     # ... (you can add more information from the session as needed)

#     # Send a confirmation email to the user
#     subject = 'Order Confirmation'
#     message = f'Thank you for your order!\n\nDetails:\n\n'
#     for item in citems:
#         message += f'{item["qty"]} x {item["name"]} - #{item["uqty"]}\n'
#     message += f'\nTotal: #{request.session.get("totalsum", 0) + request.session.get("delivery_fee", 0)}'
#     message += f'\nDelivery Address: {delivery_address}'

#     # send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email])
#     #Instead of send_mail
#     print(f"Subject: {subject}")
#     print(f"Message: {message}")
#     print(f"Sender: {settings.EMAIL_HOST_USER}")
#     print(f"Recipient: {user_email}")

#     # Assuming you have a purchase instance identified by order_id
#     purchase = Purchase.objects.get(id=order_id)
#     purchase.status = 'PAID'

# # Update the total_amount_paid field from Paystack webhook data
#     amount_paid = webhook_data.get('data', {}).get('amount') / 100  # Convert from kobo to naira
#     purchase.total_amount_paid = amount_paid

#     purchase.save()





#     if 'usercart' in request.session:
#         del request.session['usercart']
    

#      # Clear other session data
#     request.session.pop('citems', None)
#     request.session.pop('totalsum', None)
#     request.session.pop('delivery_fee', None)
#     request.session.pop('delivery_address', None)

#         # Save the session after modifying it
#     request.session.save()


   

      




#     # # Clear the cart and related session data
#     # request.session.pop('citems', None)
#     # request.session.pop('totalsum', None)
#     # request.session.pop('delivery_fee', None)
#     # request.session.pop('delivery_address', None)


#     # # Save the session after modifying it
#     # request.session.save()

#     # ... (you can add more cleanup code as needed)

#     return render(request, 'sitepages/order_success.html', {
#         'citems': citems,
#         'delivery_address': delivery_address,
#         'user_email': user_email,
#         # ... (you can pass more information to the template)
#     })



#my normal checkout that's working
# paystack_secret_key = settings.PAYSTACK_SECRET_KEY
# paystack.api_key = paystack_secret_key

# @login_required
# def checkout(request):
#     totalsum = request.session.get('totalsum', 0)
#     delivery_fee = request.session.get('delivery_fee', 0)
#     citems = request.session.get('citems', [])
#      # Your additional data
#     data = {"ptitle": "Meals order & bookings - Checkout page"}
    

#     if request.method == 'POST':
#         form = CheckoutForm(request.POST)

#         if form.is_valid():
#             with transaction.atomic():
#                 # Store delivery address in the session
#                 request.session['delivery_address'] = form.cleaned_data['delivery_address']
#                 purchase, created = Purchase.objects.get_or_create(
#                     user=request.user,
#                     status='PENDING',
#                     defaults={
#                         'order_date': timezone.now(),
#                         'delivery_address': form.cleaned_data['delivery_address'],
#                         'phone_number': form.cleaned_data['phone_number'],
#                     }
#                 )

#                 if not created:
#                     purchase.delivery_address = form.cleaned_data['delivery_address']
#                     purchase.phone_number = form.cleaned_data['phone_number']
#                     purchase.save()

#                 checkout_details = CheckoutDetails(
#                     user=request.user,
#                     full_name=form.cleaned_data['full_name'],
#                     email=form.cleaned_data['email'],
#                     delivery_address=form.cleaned_data['delivery_address'],
#                     phone_number=form.cleaned_data['phone_number'],
#                     created_at=timezone.now(),
#                 )
#                 checkout_details.save()

#                 for item in citems:
#                     OrderItem.objects.create(
#                         purchase=purchase,
#                         product_name=item['name'],
#                         quantity=item['qty'],
#                         unit_price=item['u_price'],
#                         total_price=item['uqty']
#                     )

#                     # Print each item to the console
#                     print(f"Cart item: {item}")

#                 total_amount = totalsum + delivery_fee

#                 # Redirect to the initiate_payment page with the necessary details
#                 return redirect('sitepages:initiate_payment', order_id=purchase.id, total_amount=total_amount, email=form.cleaned_data['email'])
#     else:
#         form = CheckoutForm()

#     return render(request, 'sitepages/checkout.html', {
#         'form': form,
#         'delivery_fee': delivery_fee,
#         'totalsum': totalsum,
#         'citems': citems,
#         'data': data,
#     })












































