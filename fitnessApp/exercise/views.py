from django.shortcuts import render, get_object_or_404
from .models import Exercise, Tag
from django.http import JsonResponse
import json


# Create your views here.
def exercise_list(request):
    exercises = Exercise.objects.all()
    return render(request, 'exercises.html', {'exercises': exercises})

def exercise_detail(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    return render(request, 'exercise_detail.html', {'exercise': exercise})


def create_exercise(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Extract data from the 'data' dictionary
            name = data.get('name')
            description = data.get('description')
            duration = data.get('duration')
            image_url = data.get('image_url')
            difficulty = data.get('difficulty')
            tags = data.get('tags', [])
            
            # Create the exercise instance and save it
            exercise = Exercise.objects.create(
                name=name,
                description=description,
                duration=duration,
                image_url=image_url,
                difficulty=difficulty
            )
            exercise.tags.set(create_tags(tags))

            return JsonResponse({'success': True, 'message': 'Exercise created successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON format'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

# You may need to create a method to handle tag creation
def create_tags(tag_names):
    tags = []
    for name in tag_names:
        tag, created = Tag.objects.get_or_create(name=name.strip())
        tags.append(tag)
    return tags