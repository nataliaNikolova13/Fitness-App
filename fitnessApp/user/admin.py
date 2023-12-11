from django.contrib import admin
from user.models import Goal
from user.models import ProblemArea
from user.models import UserProfile

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Goal)
admin.site.register(ProblemArea)