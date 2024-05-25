from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CustomerRegistrationForm, CinemaAdminRegistrationForm

class CustomerRegistrationView(CreateView):
    form_class = CustomerRegistrationForm
    template_name = 'registration/customer_register.html'
    success_url = reverse_lazy('login')

class CinemaAdminRegistrationView(CreateView):
    form_class = CinemaAdminRegistrationForm
    template_name = 'registration/admin_register.html'
    success_url = reverse_lazy('login')
