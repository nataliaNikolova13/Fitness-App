# urls.py

from django.urls import path
from .views import exercise_list, exercise_detail, create_exercise, create_tag

urlpatterns = [
    path('<int:exercise_id>/', exercise_detail, name='exercise_detail'),
    path('create/exercise', create_exercise, name='create_exercise'),
    path('create/tag/', create_tag, name='create_tag'),
    path('', exercise_list, name='exercise_list'),
]