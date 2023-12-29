# from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse

# Create your views here.
from .models import UserProfile

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)    
        if user is not None:
            login(request, user)
            return redirect('/workouts/')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid login credentials'})

    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('/')