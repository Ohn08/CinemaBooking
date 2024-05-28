import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from bookersapp.models import Movie, Show, Cinema


class Command(BaseCommand):
    help = 'Populate the database with sample movies, cinemas, and shows'

    def handle(self, *args, **kwargs):
        cinemas = [
            {'name': 'Labsky Theaters',
                'location': 'Puerto Princesa City', 'is_premium': True},
            {'name': 'Manila Watchroom', 'location': 'Manila', 'is_premium': False},
        ]

        for cinema_data in cinemas:
            Cinema.objects.create(**cinema_data)

        # Create sample movies
        movies = [
            {
                'title': 'The Dark Knight',
                'description': 'When the menace known as the Joker emerges from his mysterious past, he wreaks havoc and chaos on the people of Gotham.',
                'genre': 'Action',
                'release_date': datetime(2008, 7, 18).date(),
                'picture': None,
                'trailer_link': 'https://www.youtube.com/watch?v=EXeTwQWrcwY',
                'price': 299.99
            },
            {
                'title': 'The Shawshank Redemption',
                'description': 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.',
                'genre': 'Drama',
                'release_date': datetime(1994, 9, 23).date(),
                'picture': None,
                'trailer_link': 'https://www.youtube.com/watch?v=6hB3S9bIaco',
                'price': 499.99
            },
            # Add more movies as needed
        ]

        for movie_data in movies:
            Movie.objects.create(**movie_data)

        # Create sample shows
        cinemas = Cinema.objects.all()
        if not cinemas:
            self.stdout.write(self.style.WARNING(
                'No cinemas found. Please add some cinemas first.'))
            return

        for cinema in cinemas:
            for movie in Movie.objects.all():
                show_time = timezone.now() + timedelta(days=random.randint(0, 10),
                                                       hours=random.randint(0, 23))
                show, created = Show.objects.get_or_create(
                    cinema=cinema,
                    movie=movie,
                    defaults={
                        'show_time': show_time,
                    },
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(
                        f'Successfully created show for {movie.title} at {cinema.name} on {show_time}'))

        self.stdout.write(self.style.SUCCESS(
            'Successfully populated the database with sample movies, cinemas, and shows'))
