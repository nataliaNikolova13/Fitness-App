from django.contrib.auth.models import User  # Assuming you are using the built-in User model
from .models import Exercise, Workout  # Adjust this import based on your app's structure
from random import sample
import random



def create_legs_workout_function(user_profile):
    # Get exercises with the 'legs' tag
    leg_exercises = Exercise.objects.filter(tags__name='Legs')

    # Ensure there are enough leg exercises
    # if leg_exercises.count() < 5:
    #     # Handle the case where there are not enough leg exercises
    #     return None

    # Randomly select 10 unique leg exercises
    selected_leg_exercises = random.sample(list(leg_exercises), min(5, leg_exercises.count()))

    # Create a new workout and add the selected exercises
    new_workout = Workout.objects.create(user=user_profile, name="Leg workout", completed=False, category=1)
    new_workout.exercises.add(*selected_leg_exercises)
    # new_workout.exercises.set(selected_leg_exercises)
    # # new_workout.user = user
    # new_workout.completed = False
    # new_workout.name = "Leg workout"
    # new_workout.category = 1

    return new_workout