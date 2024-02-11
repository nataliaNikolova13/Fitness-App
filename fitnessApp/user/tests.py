from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile, Goal, ProblemArea
from exercise.models import Tag, UserTagCount
from .forms import RegistrationForm, UserProfileForm
from .decorators import guest_required
from django.contrib import messages
from functools import wraps

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



class GuestRequiredDecoratorTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_guest_required_redirects_authenticated_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('user_login'))
        self.assertRedirects(response, '/')

    def test_guest_required_allows_guest_user(self):
        response = self.client.get(reverse('user_login'))
        self.assertEqual(response.status_code, 200)


class SuperuserRequiredDecoratorTest(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_user(username='admin', password='adminpass', is_superuser=True)
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.factory = RequestFactory()

    def test_superuser_required_allows_superuser(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, 200)


    def test_superuser_required_denies_regular_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('user_list'))
        self.assertRedirects(response, '/')

        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].message, "Permission Denied. You must be a superuser.")
