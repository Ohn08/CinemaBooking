from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('booking/', views.booking, name='booking'),
    path('booking/<int:show_id>/', views.booking_form, name='booking_form'),
    # Other URL patterns
]
