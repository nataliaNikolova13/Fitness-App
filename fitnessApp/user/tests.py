from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile, Goal, ProblemArea
from exercise.models import Tag
from .forms import RegistrationForm, UserProfileForm
from .decorators import guest_required

# Create your tests here.

class TestUserViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_profile = UserProfile.objects.create(user=self.user, points=0)

    def test_user_login_view(self):
        response = self.client.get(reverse('user_login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')    

    def test_user_login_view_post_success(self):
        response = self.client.post(
            reverse('user_login'),
            {'username': 'testuser', 'password': 'testpassword'},
        )
        self.assertEqual(response.status_code, 302)  
        self.assertRedirects(response, reverse('workouts:user_workouts'))

    def test_user_login_view_post_failure(self):
        response = self.client.post(reverse('user_login'), {'username': 'testuser', 'password': 'invalidpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        
    def test_user_logout_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('user_login'))
        self.assertEqual(response.status_code, 302)  
        self.assertRedirects(response, reverse('homePage'))   

    def test_registration_view(self):
        response = self.client.get(reverse('registration_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    # def test_registration_view_post_success(self):
    #     response = self.client.post(
    #         reverse('registration_view'),
    #         {'username': 'newuser', 'password1': 'newpassword123', 'password2': 'newpassword123', 'email': 'newuserrr@gamil.com'},
    #     )
    #     self.assertEqual(response.status_code, 302)  
    #     # self.assertRedirects(response, reverse('user_login')) 