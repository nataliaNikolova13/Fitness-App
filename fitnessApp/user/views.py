# from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import UserProfile, Goal, ProblemArea
from .forms import RegistrationForm, UserCreationForm, UserProfileForm
from exercise.models import Tag
from workout.utils import create_legs_workout_function, create_arms_workout_function, create_cardio_workout_function, create_core_workout_function, create_custom_workout_function

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

def registration_view(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            
            goals = user_form.cleaned_data['goals']
            print(goals)
            for goal in goals:
                tag = Tag.objects.get(name=goal)
                Goal.objects.create(user=user, tag=tag)

            problem_areas = user_form.cleaned_data['problem_areas']
            for problem_area in problem_areas:
                tag = Tag.objects.get(name=problem_area)
                ProblemArea.objects.create(user=user, tag=tag)

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.points = 0
            profile.save()

            create_legs_workout_function(profile)
            create_arms_workout_function(profile)
            create_cardio_workout_function(profile)
            create_core_workout_function(profile)
            create_custom_workout_function(profile)

            return redirect('login.html')  
    else:
        user_form = RegistrationForm()
        profile_form = UserProfileForm()

    return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form})