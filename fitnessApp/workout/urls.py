from django.urls import path
from .views import create_legs_workout_view

app_name = 'workouts'

urlpatterns = [
    path('create-leg-workout/', create_legs_workout_view, name='create_legs_workout'),

    # Add other urlpatterns as needed
]