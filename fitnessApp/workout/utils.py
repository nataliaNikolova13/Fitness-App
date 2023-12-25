from django.contrib.auth.models import User  # Assuming you are using the built-in User model
from .models import Exercise, Workout  # Adjust this import based on your app's structure
from user.models import ProblemArea
from random import sample
from django.db.models import Q
from exercise.models import UserTagCount

import random


def updateUserInfo(workout):
    for exercise in workout.exercises.all():
        exercise_tags = exercise.tags.all()

        for tag in exercise_tags:
            user_tag_count, created = UserTagCount.objects.get_or_create(
                user=workout.user.user,
                tag=tag.name  # Replace with the actual field name of the tag
            )
            user_tag_count.increment_count()

    user = workout.user
    user.points += workout.exercises.count()
    user.save()        

#ARMS'),(3, 'CORE'),(4, 'CARDIO

def create_legs_workout_function(user_profile):
    leg_exercises = Exercise.objects.filter(tags__name='Legs')

    difficulty_levels = [
        (0, 'EASY'),
        (50, 'MEDIUM'),
        (100, 'HARD'),
        (200, 'PRO')
    ]

    difficulty_points = None
    for points, level in difficulty_levels:
        if user_profile.points >= points:
            difficulty_points = points
        else:
            break

    if difficulty_points is None:
        return None
    
    if leg_exercises.count() < 5:
        return None
    
    user_problem_area_tags = user_profile.problem_areas.values_list('tag__name', flat=True)

    # Exclude exercises with tags associated with user's problem areas
    excluded_exercises = leg_exercises.filter(tags__name__in=user_problem_area_tags)
    
    # Filter leg exercises with difficulty less than the user's points
    filtered_leg_exercises = leg_exercises.exclude(Q(id__in=excluded_exercises.values_list('id', flat=True)))
    
    
    if filtered_leg_exercises.count() < 5:
        return None
    
    selected_leg_exercises = random.sample(list(filtered_leg_exercises), min(5, filtered_leg_exercises.count()))
    
    new_workout = Workout.objects.create(user=user_profile, name="Leg workout", completed=False, category=1)
    new_workout.exercises.add(*selected_leg_exercises)
    
    try:
        new_workout.save()
        
        print("Workout saved successfully!")
    except Exception as e:
        print(f"Error saving workout: {e}")

    return new_workout


