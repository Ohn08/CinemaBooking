from django.contrib import admin
from .models import CinemaAdmin, Cinema, Movie, Show, Customer, Ticket, Payment, Booking, Collection

class CinemaAdminAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
    search_fields = ('user__username', 'phone_number')

admin.site.register(CinemaAdmin, CinemaAdminAdmin)

class CinemaAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'admin')
    search_fields = ('name', 'location', 'admin__user__username')

admin.site.register(Cinema, CinemaAdmin)

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'release_date')
    search_fields = ('title', 'genre')

admin.site.register(Movie, MovieAdmin)

class ShowAdmin(admin.ModelAdmin):
    list_display = ('cinema', 'movie', 'show_time', 'is_showing')
    search_fields = ('cinema__name', 'movie__title')

admin.site.register(Show, ShowAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
    search_fields = ('user__username', 'phone_number')

admin.site.register(Customer, CustomerAdmin)

class TicketAdmin(admin.ModelAdmin):
    list_display = ('seat_no', 'movie', 'show', 'price')
    search_fields = ('seat_no', 'movie__title', 'show__cinema__name')

admin.site.register(Ticket, TicketAdmin)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('method', 'amount', 'date')
    search_fields = ('method',)

admin.site.register(Payment, PaymentAdmin)

class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer', 'ticket', 'payment', 'booking_date')
    search_fields = ('customer__user__username', 'ticket__seat_no')

admin.site.register(Booking, BookingAdmin)

class CollectionAdmin(admin.ModelAdmin):
    list_display = ('customer', 'created_at')
    search_fields = ('customer__user__username',)

admin.site.register(Collection, CollectionAdmin)
