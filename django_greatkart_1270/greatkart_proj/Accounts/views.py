from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Account
from django.contrib.auth import logout


# Create your views here.
def signin(request):
    return render(request, 'signin.html')

def register(request):
    return render(request, 'register.html')





def register_view(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')  # Replace with your URL name

        if Account.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('register')

        if Account.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('register')

        # Create the user
        user = Account.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Account created successfully. You can log in now.")
        return redirect('signin')  # Replace with your login URL name

    return render(request, 'register.html')  # Replace with your actual template

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # this is the 'name' from input field
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # replace with your actual home page name
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('signin')  # replace with your actual login URL name

    return render(request, 'signin.html')


def logout_view(request):
    logout(request)  # This logs the user out
    return redirect('signin') 