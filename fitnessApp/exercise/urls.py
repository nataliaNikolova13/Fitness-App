# urls.py

from django.urls import path
from .views import exercise_list, exercise_detail

urlpatterns = [
    path('', exercise_list, name='exercise_list'),
    path('<int:exercise_id>/', exercise_detail, name='exercise_detail')

]