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


class UserProfileEditForm(forms.ModelForm):
    goals = forms.ModelMultipleChoiceField(queryset=Tag.objects.all().distinct(), widget=forms.CheckboxSelectMultiple, required=False)
    problem_areas = forms.ModelMultipleChoiceField(queryset=Tag.objects.all().distinct(), widget=forms.CheckboxSelectMultiple, required=False)

    class Meta:
        model = UserProfile
        fields = ['goals', 'problem_areas', 'bio']   

    def __init__(self, *args, **kwargs):
        super(UserProfileEditForm, self).__init__(*args, **kwargs)
        
        if self.instance:
            # Get the IDs of selected goals and problem areas
            selected_goals = self.instance.goals.values_list('id', flat=True)
            selected_problem_areas = self.instance.problem_areas.values_list('id', flat=True)

            # Set the initial values for the form fields
            self.fields['goals'].initial = selected_goals
            self.fields['problem_areas'].initial = selected_problem_areas  
            