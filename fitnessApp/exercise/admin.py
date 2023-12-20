from django.contrib import admin
from .models import Tag, Exercise

# Register your models here.

class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(Exercise, ExerciseAdmin)

admin.site.register(Tag)
# admin.site.register(Exercise)