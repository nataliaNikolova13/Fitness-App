# from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import UserProfile, Goal, ProblemArea
from .forms import RegistrationForm, UserCreationForm, UserProfileForm, UserProfileEditForm
from exercise.models import Tag
from workout.utils import create_legs_workout_function, create_arms_workout_function, create_cardio_workout_function, create_core_workout_function, create_custom_workout_function

# Create your views here.
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from .decorators import guest_required, superuser_required, user_owner_required, user_owner_or_superuser_required

@superuser_required
def user_list(request):
    profiles = UserProfile.objects.all()
    return render(request, 'users.html', {'profiles':profiles})

@user_owner_or_superuser_required
def user_detail(request, profile_id):
    profile = get_object_or_404(UserProfile, id=profile_id)
    return render(request, 'profile_detail.html', {'profile':profile})

@guest_required
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

@login_required(login_url='/user/login/')
def user_logout(request):
    logout(request)
    return redirect('/')

@guest_required
def registration_view(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.points = 0
            profile.save()
            
            goals = profile_form.cleaned_data['goals']
            print(goals)
            for goal in goals:
                tag = Tag.objects.get(name=goal)
                goal_obj = Goal.objects.create(user=user, tag=tag)
                profile.goals.add(goal_obj)

            problem_areas = profile_form.cleaned_data['problem_areas']
            for problem_area in problem_areas:
                tag = Tag.objects.get(name=problem_area)
                ProblemArea.objects.create(user=user, tag=tag)

            profile.save()

            create_legs_workout_function(profile)
            create_arms_workout_function(profile)
            create_cardio_workout_function(profile)
            create_core_workout_function(profile)
            create_custom_workout_function(profile)

            return redirect('/user/login/')  
    else:
        user_form = RegistrationForm()
        profile_form = UserProfileForm()

    return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form})


def profile_edit(request, profile_id):
    profile = get_object_or_404(UserProfile, id=profile_id)

    if request.method == 'POST':
        form = UserProfileEditForm(request.POST, instance=profile)
        if form.is_valid():

            # profile = form.save()

            # # Clear existing goals and problem areas
            # profile.goals.clear()
            # profile.problem_areas.clear()
           
            goals = form.cleaned_data['goals']
            print(goals)
            for goal in goals:
                tag = Tag.objects.get(name=goal)
                goal_obj = Goal.objects.create(user=profile.user, tag_id=tag.id)
                profile.goals.add(goal_obj)

            problem_areas = form.cleaned_data['problem_areas']
            print(problem_areas)
            for problem_area in problem_areas:
                tag = Tag.objects.get(name=problem_area)
                problem_obj = ProblemArea.objects.create(user=profile.user, tag_id=tag.id)
                profile.problem_areas.add(problem_obj)

            # form.save()
            return redirect('user_detail', profile_id=profile.id)

    else:
        form = UserProfileEditForm(instance=profile)

    return render(request, 'profile_edit.html', {'profile': profile, 'form': form})