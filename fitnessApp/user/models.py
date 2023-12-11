from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from exercise.models import Tag  

# Create your models here.

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


class ProblemArea(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)    
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

class UserProfile(models.Model):    
    bio = models.TextField(blank=True)
    email = models.EmailField(unique=True) 
    points = models.PositiveIntegerField(default=0)
    goals = models.ManyToManyField(Goal, related_name='users', blank=True)
    problem_areas = models.ManyToManyField(ProblemArea, related_name='users', blank=True)

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        # Clear existing goals to replace them with the provided list
        self.goals.clear()

        # Add provided goals
        if self.goals_input:
            goals_list = [goal.strip() for goal in self.goals_input.split(',')]
            for goal in goals_list:
                goal_obj, created = Goal.objects.get_or_create(name=goal.lower())
                self.goals.add(goal_obj)

        # Clear existing problem areas to replace them with the provided list
        self.problem_areas.clear()

        # Add provided problem areas
        if self.problem_areas_input:
            problem_areas_list = [area.strip() for area in self.problem_areas_input.split(',')]
            for area in problem_areas_list:
                area_obj, created = ProblemArea.objects.get_or_create(name=area.lower())
                self.problem_areas.add(area_obj)

        super().save(*args, **kwargs)

    @property
    def goals_input(self):
        return self._goals_input

    @goals_input.setter
    def goals_input(self, value):
        self._goals_input = value

    @property
    def problem_areas_input(self):
        return self._problem_areas_input

    @problem_areas_input.setter
    def problem_areas_input(self, value):
        self._problem_areas_input = value


