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
                tag=tag.name  
            )
            user_tag_count.increment_count()

    user = workout.user
    user.points += workout.exercises.count()
    user.save()      


    categoryNum = workout.category
    category = ''
    if categoryNum == 1:
        category = 'Legs'
    elif categoryNum == 2:
        category = 'Arms' 
    elif categoryNum == 3:
        category = 'Core'        
    elif categoryNum == 4:
        category = 'Cardio'    
    elif categoryNum == 0:
        category = 'Custom'   

    new_exercises = getExercises(workout.user, category)
    if new_exercises is not None:
        workout.exercises.clear()
        workout.exercises.add(*new_exercises) 
        workout.completed = False
        workout.save()       

  

#ARMS'),(3, 'CORE'),(4, 'CARDIO custom
    

def getExercises(user_profile, category):
    exercises = Exercise.objects.filter(tags__name=category)
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
    
    if exercises.count() < 5:
        return None    
    
    filtered_exercises = exercises.filter(difficulty__lte=difficulty_points)
    user_problem_area_tags = user_profile.problem_areas.values_list('tag__name', flat=True)
    excluded_exercises = filtered_exercises.filter(tags__name__in=user_problem_area_tags)
    filtered_exercises = filtered_exercises.exclude(Q(id__in=excluded_exercises.values_list('id', flat=True)))

    if filtered_exercises.count() < 5:
        return None
    
    selected_exercises = random.sample(list(filtered_exercises), min(5, filtered_exercises.count()))

    return selected_exercises


def create_legs_workout_function(user_profile):
    leg_exercises = getExercises(user_profile, 'Legs')
    new_workout = Workout.objects.create(user=user_profile, name="Leg workout", completed=False, category=1)
    new_workout.exercises.add(*leg_exercises)
    
    try:
        new_workout.save()
        
        print("Workout saved successfully!")
    except Exception as e:
        print(f"Error saving workout: {e}")

    return new_workout


def create_arms_workout_function(user_profile):
    arm_exercises = getExercises(user_profile, 'Arms')

    new_workout = Workout.objects.create(user=user_profile, name="Arm workout", completed=False, category=2)
    new_workout.exercises.add(*arm_exercises)
    
    try:
        new_workout.save()
        
        print("Workout saved successfully!")
    except Exception as e:
        print(f"Error saving workout: {e}")

    return new_workout


def create_core_workout_function(user_profile):
    core_exercises = getExercises(user_profile, 'Core')

    new_workout = Workout.objects.create(user=user_profile, name="Core workout", completed=False, category=2)
    new_workout.exercises.add(*core_exercises)
    
    try:
        new_workout.save()
        
        print("Workout saved successfully!")
    except Exception as e:
        print(f"Error saving workout: {e}")

    return new_workout


def create_cardio_workout_function(user_profile):
    cardio_exercises = getExercises(user_profile, 'Cardio')

    new_workout = Workout.objects.create(user=user_profile, name="Cardio workout", completed=False, category=2)
    new_workout.exercises.add(*cardio_exercises)
    
    try:
        new_workout.save()
        
        print("Workout saved successfully!")
    except Exception as e:
        print(f"Error saving workout: {e}")

    return new_workout


def create_custom_workout_function(user_profile):
    most_used_tags = UserTagCount.objects.filter(user=user_profile.user).order_by('-count')[:5]

    if not most_used_tags:
        most_used_tags = user_profile.goals.values_list('tag__name', flat=True)


    custom_exercises = Exercise.objects.filter(tags__name__in=[tag.tag for tag in most_used_tags])

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
    
    if custom_exercises.count() < 5:
        return None    
    
    filtered_exercises = custom_exercises.filter(difficulty__lte=difficulty_points)
    
    user_problem_area_tags = user_profile.problem_areas.values_list('tag__name', flat=True)
    excluded_exercises = filtered_exercises.filter(tags__name__in=user_problem_area_tags)
    filtered_exercises = filtered_exercises.exclude(Q(id__in=excluded_exercises.values_list('id', flat=True)))

    if filtered_exercises.count() < 5:
        return None
    
    selected_exercises = random.sample(list(filtered_exercises), min(10, filtered_exercises.count()))

    new_workout = Workout.objects.create(user=user_profile, name="Custom workout", completed=False, category=0)
    new_workout.exercises.add(*selected_exercises)
    
    try:
        new_workout.save()
        
        print("Workout saved successfully!")
    except Exception as e:
        print(f"Error saving workout: {e}")

    return new_workout