from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, logout
from django.contrib.auth.decorators import login_required
from .models import *



def user_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        role = request.POST['role']

        # Check if the username is unique
        if not User.objects.filter(username=username).exists():
            # Create a new user
            user = User.objects.create_user(username=username,
                                            password=password,
                                            email=email)
            profile = UserProfile.objects.create(user=user, role=role)
            profile.save()
            return redirect('user_login')  # Redirect to your login view
        else:
            error_message = 'Username already exists'
    else:
        error_message = None

    return render(request, 'auth/register.html', {'error_message': error_message})

from django.views.decorators.csrf import csrf_exempt 

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')  # Redirect to your dashboard view
        else:
            error_message = 'Invalid username or password'
    else:
        error_message = None

    return render(request, 'auth/login.html',
                  {'error_message': error_message})


def user_logout(request):
    logout(request)
    return redirect('user_login')  # Redirect to your login view