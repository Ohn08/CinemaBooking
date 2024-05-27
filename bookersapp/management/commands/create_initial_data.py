import os
from datetime import timedelta
from django.utils import timezone
from django.core.management.base import BaseCommand
from bookersapp.models import Cinema, Movie, Show, Payment, Booking

class Command(BaseCommand):
    help = 'Create initial data for the database'

    def handle(self, *args, **kwargs):
        self.create_initial_data()

    def create_initial_data(self):
        # Create initial cinemas
        cinema1 = Cinema.objects.create(name='Cinema One', location='123 Main St')
        cinema2 = Cinema.objects.create(name='Cinema Two', location='456 Elm St')

        # Create initial movies
        movie1 = Movie.objects.create(
            title='Movie One',
            description='Description for Movie One',
            genre='Action',
            release_date=timezone.now().date() - timedelta(days=10),
            picture=None,
            trailer_link='https://example.com/trailer1'
        )

        movie2 = Movie.objects.create(
            title='Movie Two',
            description='Description for Movie Two',
            genre='Comedy',
            release_date=timezone.now().date() - timedelta(days=20),
            picture=None,
            trailer_link='https://example.com/trailer2'
        )

        # Create initial shows
        show1 = Show.objects.create(
            cinema=cinema1,
            movie=movie1,
            show_time=timezone.now() + timedelta(days=1),
            is_showing=True
        )

        show2 = Show.objects.create(
            cinema=cinema2,
            movie=movie2,
            show_time=timezone.now() + timedelta(days=2),
            is_showing=True
        )

        # Create initial payments
        payment1 = Payment.objects.create(method='credit_card', amount=10.00)
        payment2 = Payment.objects.create(method='cash', amount=15.00)

        # Create initial bookings
        booking1 = Booking.objects.create(
            seat_no='A1',
            show=show1,
            price=12.00,
            payment=payment1
        )

        booking2 = Booking.objects.create(
            seat_no='B2',
            show=show2,
            price=10.00,
            payment=payment2
        )

        self.stdout.write(self.style.SUCCESS('Initial data created successfully.'))
