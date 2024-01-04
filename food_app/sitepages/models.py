from django.db import models
#
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal



# Create your models here.
class FoodItem(models.Model):
    name=models.CharField(max_length=100)
    desc_short=models.CharField(max_length=100)
    desc_long=models.TextField()
    price=models.CharField(max_length=10)
    image=models.ImageField(upload_to="uploaded")

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

    # Other fields and methods as needed

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
















