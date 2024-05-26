from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, AdminRegisterForm
from .models import CinemaAdmin, Show, Payment, Ticket, Booking, Movie

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def admin_register(request):
    if request.method == 'POST':
        form = AdminRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            phone_number = form.cleaned_data.get('phone_number')
            CinemaAdmin.objects.create(user=user, phone_number=phone_number)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('admin_dashboard')
    else:
        form = AdminRegisterForm()
    return render(request, 'admin_register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def book_ticket(request, show_id):
    show = get_object_or_404(Show, id=show_id)
    if request.method == 'POST':
        seat_no = request.POST['seat_no']
        price = request.POST['price']
        payment_method = request.POST['payment_method']
        amount = request.POST['amount']
        
        # Create payment
        payment = Payment.objects.create(method=payment_method, amount=amount)

        # Create ticket and booking
        ticket = Ticket.objects.create(seat_no=seat_no, movie=show.movie, show=show, price=price)
        booking = Booking.objects.create(customer=request.user.customer, ticket=ticket, payment=payment)

        return redirect('booking_success')
    return render(request, 'book_ticket.html', {'show': show})

@login_required
def admin_dashboard(request):
    try:
        cinema_admin = request.user.cinemaadmin
    except CinemaAdmin.DoesNotExist:
        return redirect('home')
    return render(request, 'admin_dashboard.html')

def movies_list(request):
    movies = Movie.objects.all()
    return render(request, 'movies_list.html', {'movies': movies})

@login_required
def profile_view(request):
    user = request.user  
    return render(request, 'profile.html', {'user': user})