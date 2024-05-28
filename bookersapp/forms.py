from django import forms
from bookersapp.models import Booking, Payment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field


class BookingForm(forms.ModelForm):
    payment_method = forms.ChoiceField(choices=Payment.PAYMENT_CHOICES)
    payment_amount = forms.DecimalField()

    class Meta:
        model = Booking
        fields = ['seat_no']

    def __init__(self, *args, **kwargs):
        # Get the show instance from kwargs
        self.show = kwargs.pop('show', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('seat_no'),
            Field('payment_method'),
            Field('payment_amount'),
        )

    def clean(self):
        cleaned_data = super().clean()
        payment_amount = cleaned_data.get('payment_amount')
        print(self.show)
        if payment_amount and payment_amount < self.show.calculate_price:
            raise forms.ValidationError(
                "Payment amount should be at least equal to the price of the show.")
        return cleaned_data
