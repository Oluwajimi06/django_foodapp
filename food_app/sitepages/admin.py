from django.contrib import admin
from .models import*

# Register your models here.
admin.site.register(FoodItem)
admin.site.register(Purchase)
admin.site.register(OrderItem)
# admin.site.register(OrderHistory)
admin.site.register(CheckoutDetails)





