from django.db import models

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
    image_url = models.URLField(null=True, blank=True)
    difficulty = models.IntegerField(choices=DIFFICULTY, default=0)
    tags = models.ManyToManyField('Tag', related_name='exercises', blank=True)


    def save(self, *args, **kwargs):
        # Clear existing tags to replace them with the provided list
        self.tags.clear()

        # Add provided tags
        if self.tags_input:
            tags_list = [tag.strip() for tag in self.tags_input.split(',')]
            for tag in tags_list:
                tag_obj, created = Tag.objects.get_or_create(name=tag.lower())
                self.tags.add(tag_obj)

        super().save(*args, **kwargs)

    @property
    def tags_input(self):
        return self._tags_input

    @tags_input.setter
    def tags_input(self, value):
        self._tags_input = value


    def __str__(self):
        return self.name

