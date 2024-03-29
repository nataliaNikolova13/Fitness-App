"""
URL configuration for fitnessApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from common.views import homePage, custom_404
from exercise.views import exercise_list
from user.views import login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('exercise/', include('exercise.urls')),
    path('user/', include('user.urls')),
    path('workouts/', include('workout.urls'), name='workouts'),
    path('posts/', include('feed.urls')),
    path('', homePage, name='homePage'),
]

handler404 = custom_404
 