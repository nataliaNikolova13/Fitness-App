from django.shortcuts import render, get_object_or_404
from .models import Exercise

# Create your views here.
def exercise_list(request):
    exercises = Exercise.objects.all()
    return render(request, 'exercises.html', {'exercises': exercises})

def exercise_detail(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    return render(request, 'exercise_detail.html', {'exercise': exercise})


