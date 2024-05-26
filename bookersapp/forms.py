from django import forms
from bookersapp.models import Booking, Payment


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['seat_no', 'price']

    payment_method = forms.ChoiceField(choices=Payment.PAYMENT_CHOICES)
    payment_amount = forms.DecimalField()
