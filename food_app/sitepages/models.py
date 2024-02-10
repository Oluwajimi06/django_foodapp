from django.db import models
#
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver





# Create your models here.
class FoodItem(models.Model):
    CATEGORY_CHOICES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
    ]

    name = models.CharField(max_length=100)
    desc_short = models.CharField(max_length=100)
    desc_long = models.TextField()
    price = models.CharField(max_length=10)
    image = models.ImageField(upload_to="uploaded")
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='Breakfast')

    def __str__(self):
        return self.name








class CheckoutDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, default='')
    email = models.EmailField(default='example@example.com')
    delivery_address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"CheckoutDetails for {self.user.username}"








from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Purchase(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, default='')
    order_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    total_amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # New field to track payment status
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Purchase {self.id} - {self.user.username}"

    def calculate_total_amount(self):
        # Include delivery fee in the total amount calculation
        delivery_fee = 1500  # Replace with your actual delivery fee logic
        total_amount = sum(item.total_price for item in self.order_items.all()) + delivery_fee
        return total_amount

    @property
    def total_amount(self):
        return self.calculate_total_amount()

class OrderItem(models.Model):
    purchase = models.ForeignKey(Purchase, related_name='order_items', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"OrderItem {self.id} - {self.product_name} - {self.purchase}"





class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    delivery_address = models.TextField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()  # Include the email field

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email




class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"


class Table(models.Model):
    TABLE_TYPES = [
        ('People 1', 'People 1'),
        ('People 2', 'People 2'),
        ('People 3', 'People 3'),
    ]

    table_type = models.CharField(max_length=20, choices=TABLE_TYPES, unique=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.table_type









class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Set a default value
    table = models.ForeignKey(Table, on_delete=models.CASCADE, null=True)  # Allow null values
    booking_date = models.DateField()
    booking_time = models.TimeField()
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]

    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')

    def __str__(self):
        return f'{self.user.username} - {self.booking_date} {self.booking_time}'





class BookingHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]

    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')

    # Add any other fields as needed

    def __str__(self):
        return f'{self.user.username} - {self.booking.booking_date} {self.booking.booking_time}'












# class OrderItem(models.Model):
#     order = models.ForeignKey(NewOrder, related_name='order_items', on_delete=models.CASCADE)
#     product_name = models.CharField(max_length=255)
#     quantity = models.IntegerField()
#     unit_price = models.DecimalField(max_digits=10, decimal_places=2)
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f"OrderItem {self.id} - {self.product_name} - {self.order}"









# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
#     product_name = models.CharField(max_length=255)
#     quantity = models.IntegerField()
#     unit_price = models.DecimalField(max_digits=10, decimal_places=2)
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f"OrderItem {self.id} - {self.product_name} - {self.order}"

    # Add any additional methods or fields as needed


# class OrderHistory(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     payment_date = models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return f"OrderHistory {self.id} - Order {self.order.id} - {self.order.user.username}"

    # ... other methods or fields ...






# class Order(models.Model):
#     STATUS_CHOICES = [
#         ('PENDING', 'Pending'),
#         ('PAID', 'Paid'),
#         ('SHIPPED', 'Shipped'),
#         ('DELIVERED', 'Delivered'),
#     ]

#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     delivery_address = models.CharField(max_length=255)
#     phone_number = models.CharField(max_length=20, default='')
#     order_date = models.DateTimeField(default=timezone.now)
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

#     def calculate_total_amount(self):
#         order_items = self.orderitem_set.all()
#         total_amount = sum(item.total_price for item in order_items)
#         return total_amount

#     @property
#     def update_total_amount(self):
#         total_amount = self.calculate_total_amount()
#         self.total_amount = total_amount
#         self.save()
#         return total_amount

#     def __str__(self):
#         return f"Order {self.id} - {self.user.username}"

# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     product_name = models.CharField(max_length=255)
#     quantity = models.PositiveIntegerField()
#     unit_price = models.DecimalField(max_digits=10, decimal_places=2)
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f"OrderItem {self.id} - {self.product_name}"

# class OrderHistory(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     payment_date = models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return f"OrderHistory {self.id} - Order {self.order.id} - {self.order.user.username}"
















