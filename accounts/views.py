import re
import random
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate as auth_authenticate
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from products.models import *

# Create your views here.

def home(request):
    categories = Category.objects.all()
    return render(request, 'home.html', {'categories': categories})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = auth_authenticate(username=username, password=password)
            if user:
                auth_login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'User credentials does not match.')
                return redirect('login')

    return render(request, 'login.html')


def user_logout(request):
    auth_logout(request)
    return redirect('home')


def send_mail(request):
    otp = random.randint(0000, 9999)
    subject = 'Registration Successful!! Check OTP'
    message = (f'Hello, please do not share your OTP. Your OTP is {otp}')
    from_email = settings.EMAIL_HOST_USER
    recipient_list = []
    send_mail(subject, message, from_email, recipient_list)


def signup_otp(request):
    return render(request, 'signup_otp.html')


def user_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        retype_password = request.POST['retype_password']

        # Check if username or email is already taken
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
        # Check password length and if it contains a number
        elif len(password) < 6 or not re.search(r'\d', password):
            messages.error(request, 'Password must be at least 6 characters long and contain a number.')
        # Check if passwords match
        elif password != retype_password:
            messages.error(request, 'Passwords do not match.')
        else:
            # If validation passes, save the user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.set_password(password)
            user.save()

            # Create a cart for the user
            Cart.objects.create(user=user)

            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')

    return render(request, 'register.html')