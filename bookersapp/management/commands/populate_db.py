from django.core.management.base import BaseCommand
from bookersapp.models import Cinema, Movie, Show, Payment, Booking
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **kwargs):
        self.populate_cinemas()
        self.populate_movies()
        self.populate_shows()
        self.populate_payments()
        self.populate_bookings()
        self.stdout.write(self.style.SUCCESS(
            'Successfully populated the database with sample data.'))

    def populate_cinemas(self):
        cinema_data = [
            {'name': 'Starlight Cinemas', 'location': '123 Main Street'},
            {'name': 'Moonbeam Theater', 'location': '456 Elm Avenue'},
            {'name': 'Galaxy Multiplex', 'location': '789 Oak Boulevard'},
        ]
        for data in cinema_data:
            Cinema.objects.create(**data)

    def populate_movies(self):
        movie_titles = [
            "The Enigmatic Dreamer",
            "Echoes of the Cosmos",
            "Whispers in the Dark",
            "Chronicles of Eternity",
            "The Lost Symphony",
            "The Quantum Odyssey",
            "Spectral Serenade",
            "The Celestial Requiem",
            "Aurora's Embrace",
            "Midnight Mirage"
        ]
        for title in movie_titles:
            Movie.objects.create(
                title=title,
                description="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                genre=random.choice(
                    ['Action', 'Adventure', 'Sci-Fi', 'Thriller']),
                release_date=datetime.now().date() - timedelta(days=random.randint(30, 365)),
            )

    def populate_shows(self):
        cinemas = list(Cinema.objects.all())
        movies = list(Movie.objects.all())

        for _ in range(10):
            show_time = datetime.now() + timedelta(days=random.randint(0, 10),
                                                   hours=random.randint(0, 23))
            Show.objects.create(
                cinema=random.choice(cinemas),
                movie=random.choice(movies),
                show_time=show_time,
                is_showing=random.choice([True, False])
            )

    def populate_payments(self):
        payment_data = [
            {'method': 'credit_card', 'amount': round(
                random.uniform(10.0, 100.0), 2)},
            {'method': 'cash', 'amount': round(
                random.uniform(10.0, 100.0), 2)},
            {'method': 'mobile_banking', 'amount': round(
                random.uniform(10.0, 100.0), 2)},
        ]
        for data in payment_data:
            Payment.objects.create(**data)

    def populate_bookings(self):
        shows = list(Show.objects.all())
        payments = list(Payment.objects.all())

        for _ in range(20):
            show = random.choice(shows)
            Booking.objects.create(
                seat_no=f'S{random.randint(1, 100)}',
                show=show,
                price=round(random.uniform(10.0, 20.0), 2),
                payment=random.choice(payments) if random.choice(
                    [True, False]) else None,
                booking_date=datetime.now()
            )
