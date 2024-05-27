from django.db import models
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Cinema(BaseModel):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

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
    def get_trailer_link(self):
        return reverse('movie_trailer', kwargs={'pk': self.pk})

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
    price = models.DecimalField(max_digits=10, decimal_places=2)
    payment = models.ForeignKey(
        Payment, on_delete=models.CASCADE, null=True, blank=True)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking for {self.show.movie.title} - {self.seat_no} on {self.show.show_time}"
