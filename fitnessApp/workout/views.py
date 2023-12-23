from django.shortcuts import render
from exercise.models import Exercise
from django.http import HttpResponse
from user.models import UserProfile
from django.contrib.auth.models import User


from .models import Workout
import random
from .utils import create_legs_workout_function

# Create your views here.

def create_legs_workout_view(request):
    # You may need to adjust how you get or create a user instance
    # depending on your specific requirements
    # user_profile = UserProfile.objects.get(user=request.user)

    # just for now, don't have users

    # Get the superuser (replace 'admin' with your superuser's username)
    superuser = User.objects.get(username='nati')

    # Assuming you have a UserProfile associated with the superuser
    try:
        # user_profile = UserProfile.objects.get(user=superuser)
        user_profile, created = UserProfile.objects.get_or_create(user=superuser)
    except UserProfile.DoesNotExist:
        # Create UserProfile if it doesn't exist
        # user_profile = UserProfile.objects.create(user=superuser)
        user_profile, created = UserProfile.objects.get_or_create(user=superuser)


    # Call the function to create a leg workout
    leg_workout = create_legs_workout_function(user_profile)

    if leg_workout:
        return HttpResponse(f"Leg workout created for {user_profile.user.username}.")
    else:
        return HttpResponse("Failed to create leg workout. Not enough leg exercises.")