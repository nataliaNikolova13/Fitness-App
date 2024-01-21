from django import forms
from .models import Exercise, Tag

class CreateExerciseForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)

    class Meta:
        model = Exercise
        fields = ['name', 'description', 'duration', 'image_url', 'difficulty']

    def save(self, commit=True):
        exercise = super(CreateExerciseForm, self).save(commit=commit)
        exercise.tags.clear()
        for tag in self.cleaned_data['tags']:
            exercise.tags.add(tag)

        return exercise
    

class CreateTagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']   
