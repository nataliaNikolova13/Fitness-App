from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from exercise.models import Tag  

# Create your models here.

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return self.tag.name


class ProblemArea(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)    
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return self.tag.name

class UserProfile(models.Model):   
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None) 
    bio = models.TextField(blank=True)
    email = models.EmailField(unique=True) 
    points = models.PositiveIntegerField(default=0)
    goals = models.ManyToManyField(Goal, related_name='users', blank=True)
    problem_areas = models.ManyToManyField(ProblemArea, related_name='users', blank=True)

    def __str__(self):
        return self.user.username
    


