from django.shortcuts import render, get_object_or_404, redirect
from .models import Exercise, Tag
from django.http import JsonResponse
import json
from user.decorators import superuser_required
from .forms import CreateExerciseForm, CreateTagForm


@superuser_required
def exercise_list(request):
    exercises = Exercise.objects.all()
    return render(request, 'exercises.html', {'exercises': exercises})

def exercise_detail(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    return render(request, 'exercise_detail.html', {'exercise': exercise})

@superuser_required
def create_exercise(request):
    if request.method == 'POST':
        form = CreateExerciseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('exercise_list')  
    else:
        form = CreateExerciseForm()

    return render(request, 'create_exercise.html', {'form': form})
   


@superuser_required
def create_tag(request):
    if request.method == 'POST':
        form = CreateTagForm(request.POST)
        if form.is_valid():
            tag_name = form.cleaned_data['name']
            tag, created = Tag.objects.get_or_create(name=tag_name)
            return redirect('exercise_list')  
    else:
        form = CreateTagForm()

    return render(request, 'create_tag.html', {'form': form})   