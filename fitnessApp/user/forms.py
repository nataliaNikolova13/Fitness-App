from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Goal, ProblemArea
from exercise.models import Tag

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserProfileForm(forms.ModelForm):
    # goals = forms.ModelMultipleChoiceField(queryset=Goal.objects.values_list('tag__name', flat=True).distinct(), widget=forms.CheckboxSelectMultiple, required=False)
    goals = forms.ModelMultipleChoiceField(queryset=Tag.objects.all().distinct(), widget=forms.CheckboxSelectMultiple, required=False)
    # problem_areas = forms.ModelMultipleChoiceField(queryset=ProblemArea.objects.values_list('tag__name', flat=True).distinct(), widget=forms.CheckboxSelectMultiple, required=False)
    problem_areas = forms.ModelMultipleChoiceField(queryset=Tag.objects.all().distinct(), widget=forms.CheckboxSelectMultiple, required=False)


    class Meta:
        model = UserProfile
        fields = ['goals', 'problem_areas', 'bio']