from django.db import models
from django.contrib.auth.models import User

# Cinema Admin
class CinemaAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username

    def add_movie_showing(self, cinema, movie, show_time):
        Show.objects.create(cinema=cinema, movie=movie, show_time=show_time, is_showing=True)

    def remove_movie_showing(self, show):
        show.delete()

    def edit_ticket(self, ticket, seat_no=None, price=None):
        if seat_no:
            ticket.seat_no = seat_no
        if price:
            ticket.price = price
        ticket.save()

# Cinema
class Cinema(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    admin = models.ForeignKey(CinemaAdmin, on_delete=models.SET_NULL, null=True, blank=True, related_name='cinemas')

    def __str__(self):
        return self.name

# Movie
class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    genre = models.CharField(max_length=50)
    release_date = models.DateField()
    picture = models.ImageField(upload_to='movies/', default='default.jpg', null=True, blank=True)
    trailer_link = models.URLField(default='https://example.com/default-trailer', null=True, blank=True)

    def __str__(self):
        return self.title

# Show
class Show(models.Model):
    cinema = models.ForeignKey(Cinema, on_delete=models.SET_NULL, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.SET_NULL, null=True)
    show_time = models.DateTimeField(null=True)
    is_showing = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.movie.title} at {self.cinema.name} on {self.show_time}"


# Customer
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username

    def book_ticket(self, show, seat_no, price, payment_method, amount):
        # Create payment
        payment = Payment.objects.create(method=payment_method, amount=amount)

        # Create ticket and booking
        ticket = Ticket.objects.create(seat_no=seat_no, movie=show.movie, show=show, price=price)
        booking = Booking.objects.create(customer=self, ticket=ticket, payment=payment)
        return booking

    def cancel_ticket(self, booking):
        booking.ticket.delete()
        booking.delete()

# Ticket
class Ticket(models.Model):
    seat_no = models.CharField(max_length=10)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.movie.title} - {self.seat_no} on {self.show.show_time}"

# Payment
class Payment(models.Model):
    PAYMENT_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('cash', 'Cash'),
        ('mobile_banking', 'Mobile Banking'),
    ]

    method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.method} - {self.amount}"

# Booking
class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True, blank=True)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking for {self.customer.user.username} on {self.booking_date}"

# Collection
class Collection(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    tickets = models.ManyToManyField(Ticket)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.user.username}'s Collection"
