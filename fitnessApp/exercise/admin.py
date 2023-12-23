from django.contrib import admin
from .models import Tag, Exercise, UserTagCount

# Register your models here.

class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(UserTagCount)
admin.site.register(Tag)
# admin.site.register(Exercise)