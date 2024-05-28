from django.db import models
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Cinema(BaseModel):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Movie(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    genre = models.CharField(max_length=50)
    release_date = models.DateField()
    picture = models.ImageField(
        upload_to='movies/', default='default.jpg', null=True, blank=True)
    trailer_link = models.URLField(
        default='https://example.com/default-trailer', null=True, blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)  # Add price field

    def get_trailer_link(self):
        return reverse('movie_trailer', kwargs={'pk': self.pk})

    @property
    def image_url(self):
        if self.picture and hasattr(self.picture, 'url'):
            return self.picture.url
        return "/media/movies/default.jpg"

    def __str__(self):
        return self.title


class Show(BaseModel):
    cinema = models.ForeignKey(Cinema, on_delete=models.SET_NULL, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.SET_NULL, null=True)
    show_time = models.DateTimeField(null=True)
    is_showing = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        current_time = timezone.now()
        show_time = self.show_time
        if show_time:
            if current_time <= show_time <= current_time + timedelta(days=7):
                self.is_showing = True
            else:
                self.is_showing = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.movie.title} at {self.cinema.name} on {self.show_time}"

    @property
    def calculate_price(self):
        # Add logic to calculate price based on movie and cinema
        price = self.movie.price  # Start with movie price
        # Adjust price based on cinema, if needed
        # Example logic: Increase price by 15% if the cinema is a premium one
        if self.cinema.is_premium:
            print("Yes")
            price *= Decimal(1.15)  # Increase price by 15%
            price = round(price, 2)

        return price


class Payment(BaseModel):
    PAYMENT_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('cash', 'Cash'),
        ('mobile_banking', 'Mobile Banking'),
    ]

    method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.method} - {self.amount}"


class Booking(BaseModel):
    seat_no = models.CharField(max_length=10)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)  # Remove price field
    payment = models.ForeignKey(
        Payment, on_delete=models.CASCADE, null=True, blank=True)
    booking_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only calculate price if it's a new booking
            self.price = self.show.calculate_price
        super().save(*args, **kwargs)
