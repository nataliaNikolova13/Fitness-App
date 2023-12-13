from django.db import models
from django.utils.text import slugify

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

