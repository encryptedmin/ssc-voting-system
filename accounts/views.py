from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm
from .models import CustomUser


def landing_view(request):
    return render(request, 'accounts/landing.html')


def register_view(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            user.role = 'VOTER'
            user.is_approved = False

            user.save()

            messages.success(request, 'Registration successful. Wait for admin approval.')
            return redirect('login')

    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:

            if user.role == 'VOTER' and not user.is_approved:
                messages.error(request, 'Account pending admin approval.')
                return redirect('login')

            login(request, user)

            if user.role == 'ADMIN':
                return redirect('admin_dashboard')

            elif user.role == 'VOTER':
                return redirect('voter_dashboard')

        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')
