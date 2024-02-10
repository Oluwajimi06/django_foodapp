from django.contrib import admin
from .models import*



class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    readonly_fields = ('subscribed_at',)




class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')  # Display these fields in the admin list view


# Register your models here.
admin.site.register(FoodItem)
admin.site.register(Purchase)
admin.site.register(OrderItem)
admin.site.register(CheckoutDetails)
admin.site.register(UserProfile)
admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('table_type', 'price')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ( 'booking_date', 'booking_time', 'created_at')




class BookingHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'booking', 'timestamp', 'payment_status')
    list_filter = ('payment_status',)
    search_fields = ('user__username', 'booking__booking_date', 'booking__booking_time')

admin.site.register(BookingHistory, BookingHistoryAdmin)







