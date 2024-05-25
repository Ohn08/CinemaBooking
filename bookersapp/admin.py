from django.contrib import admin
from .models import CinemaAdmin, Movie, Customer, Ticket, Payment, Booking, Collection

admin.site.register(CinemaAdmin)
admin.site.register(Movie)
admin.site.register(Customer)
admin.site.register(Ticket)
admin.site.register(Payment)
admin.site.register(Booking)
admin.site.register(Collection)
