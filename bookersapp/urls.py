from django.urls import path, include
from django.views.generic import TemplateView
from bookersapp.views import CustomerRegistrationView, CinemaAdminRegistrationView  
urlpatterns = [
    path('register/customer/', CustomerRegistrationView.as_view(), name='customer-register'),
    path('register/admin/', CinemaAdminRegistrationView.as_view(), name='admin-register'),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),  
]
