from django.db import models
from exercise.models import Exercise
from user.models import UserProfile

# Create your models here.

CATEGORY = [
    (0, 'CUSTOM'),
    (1, 'LEGS'),
    (2, 'ARMS'),
    (3, 'CORE'),
    (4, 'CARDIO')
]

class Workout(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    exercises = models.ManyToManyField(Exercise, related_name='workout')
    category = models.IntegerField(choices=CATEGORY, default=0)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name