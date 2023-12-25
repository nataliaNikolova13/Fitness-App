from django.urls import path
from .views import user_workouts, workout_detail, mark_workout_completed

app_name = 'workouts'

urlpatterns = [
    path('', user_workouts, name='user_workouts'),
    path('workout/<int:workout_id>/', workout_detail, name='workout_detail'),
    path('workout/<int:workout_id>/mark_completed/', mark_workout_completed, name='mark_workout_completed'),

    # Add other urlpatterns as needed
]