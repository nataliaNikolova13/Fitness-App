from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from user.models import UserProfile
from .models import Workout
from exercise.models import Exercise
from exercise.models import UserTagCount, Tag
from .utils import updateUserInfo, getExercises, getExercisesCustom, create_legs_workout_function, create_arms_workout_function, create_core_workout_function, create_cardio_workout_function, create_custom_workout_function


class WorkoutViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.workout = Workout.objects.create(user=self.user_profile, name='Test Workout')

    def test_user_workouts_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('workouts:user_workouts'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('workouts', response.context)

    def test_workout_detail_view(self):
        response = self.client.get(reverse('workouts:workout_detail', args=[self.workout.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('workout', response.context)

    def test_mark_workout_completed_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('workouts:mark_workout_completed', args=[self.workout.id]))
        self.assertEqual(response.status_code, 302)
        self.workout.refresh_from_db()
        self.assertTrue(self.workout.completed)

    
class WorkoutUtilsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_profile = UserProfile.objects.create(user=self.user)

    def test_update_user_info(self):
        exercise = Exercise.objects.create(name='Test Exercise', difficulty=30)
        workout = Workout.objects.create(user=self.user_profile, name='Test Workout')
        workout.exercises.add(exercise)
        updateUserInfo(workout)
        self.user_profile.refresh_from_db()
        self.assertEqual(self.user_profile.points, 1)

    
