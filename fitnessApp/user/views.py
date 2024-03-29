# from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from .models import UserProfile, Goal, ProblemArea
from .forms import RegistrationForm, UserCreationForm, UserProfileForm, UserProfileEditForm
from exercise.models import Tag, UserTagCount
from workout.utils import create_legs_workout_function, create_arms_workout_function, create_cardio_workout_function, create_core_workout_function, create_custom_workout_function

# Create your views here.
from .models import UserProfile
from django.contrib.auth.models import User
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

            return redirect('user_detail', profile_id=profile.id)

    else:
        form = UserProfileEditForm(instance=profile)

    return render(request, 'profile_edit.html', {'profile': profile, 'form': form})


@user_owner_or_superuser_required
def user_statistics(request, profile_id):
    user_profile = get_object_or_404(UserProfile, id=profile_id)
    # user = get_object_or_404(User, id=profile_id)
    points_user = user_profile.points
    print(points_user)

    difficulty_levels = [
        (0, 'EASY'),
        (50, 'MEDIUM'),
        (100, 'HARD'),
        (200, 'PRO')
    ]

    user_level = None
    for points, level in difficulty_levels:
        if points_user >= points:
            difficulty_points = points
            user_level = level
        else:
            break

    user_tag_counts = UserTagCount.objects.filter(user = user_profile.user).order_by('-count') 

    print(user_tag_counts.values_list('tag', flat=True))

    context = {'name':user_profile.user.username, 'difficulty_points': user_level, 'user_tag_counts': user_tag_counts}
    
    return render(request, 'user_statistics.html', context)