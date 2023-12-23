from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

DIFFICULTY = [
    (0, 'EASY'),
    (50, 'MEDIUM'),
    (100, 'HARD'),
    (200, 'PRO')
]

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Create your models here.
class Exercise(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    duration = models.PositiveIntegerField(null=True, blank=True)
    image_url = models.URLField(null=True, blank=True, max_length=500)
    difficulty = models.IntegerField(choices=DIFFICULTY, default=0)
    tags = models.ManyToManyField('Tag', related_name='exercises', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    

class UserTagCount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.CharField(max_length=50)  
    count = models.PositiveIntegerField(default=0)

    def increment_count(self):
        self.count += 1
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.tag}: {self.count}"
