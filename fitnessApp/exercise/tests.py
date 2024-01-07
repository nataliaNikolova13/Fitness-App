from django.test import TestCase, Client
from django.urls import reverse
from .models import Exercise, Tag

# Create your tests here.
class TestExerciseViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.exercise = Exercise.objects.create(
            name='Test name',
            description='Test description',
            duration=30,
            image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQfKf2CTDrXCjoOgnrk7GdsF5VAHzvwI0COBQ&usqp=CAU',
            difficulty=1
        )
        self.tag = Tag.objects.create(name='Test Tag')

    def test_exercise_list_view(self):
        response = self.client.get(reverse('exercise_list'))    
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'exercises.html')
        self.assertContains(response, self.exercise.name)

    def test_exercise_detail_view(self):
        response = self.client.get(reverse('exercise_detail', args=[self.exercise.id]))    
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'exercise_detail.html')
        self.assertContains(response, self.exercise.name)

    def test_exercise_detail_view_invalid_id(self):
        invalid_id = self.exercise.id + 1
        response = self.client.get(reverse('exercise_detail', args=[invalid_id]))
        self.assertEqual(response.status_code, 404)

    def test_exercise_detail_view_nonexistent_id(self):
        nonexistent_id = 999
        response = self.client.get(reverse('exercise_detail', args=[nonexistent_id]))
        self.assertEqual(response.status_code, 404)  
