from django.contrib import admin
from .models import Cinema, Movie, Show, Payment, Booking

admin.site.register(Cinema)
admin.site.register(Movie)
admin.site.register(Show)
admin.site.register(Payment)
admin.site.register(Booking)
