from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookingForm
from .models import Show, Payment


def booking(request):
    shows = Show.objects.select_related('cinema', 'movie').all()
    return render(request, 'booking.html', {'shows': shows})


def booking_form(request, show_id):
    show = get_object_or_404(Show, pk=show_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.show = show
            booking.save()
            payment_method = form.cleaned_data.get('payment_method')
            payment_amount = form.cleaned_data.get('payment_amount')
            Payment.objects.create(method=payment_method,
                                   amount=payment_amount)
            return redirect('booking_page')
    else:
        form = BookingForm()

    return render(request, 'booking_form.html', {'form': form, 'show': show})


def home(request):
    return render(request, 'home.html')
