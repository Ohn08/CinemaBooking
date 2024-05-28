from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .forms import BookingForm
from .models import Show, Payment, Booking


def home(request):
    now_showing = Show.objects.filter(is_showing=True)
    return render(request, 'home.html', {'now_showing': now_showing})


def booking(request):
    shows = Show.objects.select_related('cinema', 'movie').all()
    return render(request, 'booking.html', {'shows': shows})


def booking_form(request, show_id):
    show = get_object_or_404(Show, pk=show_id)

    if request.method == 'POST':
        form = BookingForm(request.POST, show=show)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.show = show
            booking.save()
            payment_method = form.cleaned_data.get('payment_method')
            payment_amount = form.cleaned_data.get('payment_amount')
            # Create a Payment instance and associate it with the booking
            payment = Payment.objects.create(
                method=payment_method,
                amount=payment_amount
            )
            booking.payment = payment  # Assign the payment to the booking
            booking.save()  # Save the booking with the payment association
            return redirect('booking')
    else:
        form = BookingForm(show=show)

    return render(request, 'booking_form.html', {'form': form, 'show': show})


def booked_tickets(request):
    bookings = Booking.objects.all()
    paginator = Paginator(bookings, 10)  # Show 10 bookings per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tickets.html', {'bookings': page_obj, 'is_paginated': True})
