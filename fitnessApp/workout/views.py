from django.shortcuts import render, get_object_or_404, redirect
from exercise.models import Exercise
from django.http import HttpResponse
from user.models import UserProfile
from django.contrib.auth.models import User
from .models import Workout
from django.contrib.auth.decorators import login_required
from .utils import updateUserInfo


# Create your views here.
@login_required
def user_workouts(request):
    workouts = Workout.objects.filter(user=request.user.userprofile)
    return render(request, 'user_workouts.html', {'workouts': workouts})


def workout_detail(request, workout_id):
    workout = get_object_or_404(Workout, pk=workout_id)
    return render(request, 'workout_detail.html', {'workout': workout})


def mark_workout_completed(request, workout_id):
    workout = get_object_or_404(Workout, pk=workout_id)
    workout.completed = True
    workout.save()
    updateUserInfo(workout)
    return redirect('workouts:workout_detail', workout_id=workout.id)
