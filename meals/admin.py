from django.contrib import admin
from .models import Meal, Menu, BookingRequest, Bookings

# Register your models here.
admin.site.register(Meal)
admin.site.register(Menu)
admin.site.register(BookingRequest)
admin.site.register(Bookings)