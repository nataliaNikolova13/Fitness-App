# Fitness-App
Django Project for Python Course @ FMI

# Project Overview 
A Django Backend project that generates custom workout based previous workout history. Exercise difficulty increases based on workout progress. 

## Usage
 - Access the admin panel:
Open your browser and go to http://127.0.0.1:8000/admin/
Log in with the superuser credentials created during the installation.
 - Acess http://127.0.0.1:8000/workouts/ 
When logged in go to this url to access your custom workout routines.

## EndPoints
Fitness App Endpoints:

### Admin Interface:
 - GET /admin/: Django Admin Interface.

### Exercise Module:
 - GET /exercise/: List of exercises.
 - GET /exercise/<int:exercise_id>/: Exercise detail.
 - POST /exercise/create/exercise/: Create a new exercise.
 - POST /exercise/create/tag/: Create a new exercise tag.

### User Module:
 - POST /user/login/: User login.
 - POST /user/logout/: User logout.
 - POST /user/register/: User registration.
 - GET /user/<int:profile_id>/: User profile detail.
 - POST /user/edit/<int:profile_id>/: Edit user profile.
 - GET /user/statistics/<int:profile_id>/: User statistics.
 - GET /user/: List of users

### Workout Module:
 - GET /workouts/: List of user workouts.
 - GET /workouts/workout/<int:workout_id>/: Workout detail.
 - POST /workouts/workout/<int:workout_id>/mark_completed/: Mark workout as completed.

### Post Module:
 - GET /posts/: List of all posts.
 - POST /posts/create/: Create a new post.
 - GET /posts/<int:post_id>/: Post detail.
 - GET /posts/<str:username>/: Posts of a specific user.
 - POST /posts/like-post/<int:post_id>/: Like a post.

### Common Endpoints:
 - GET /: Homepage. 

## User Roles
### User
 - Can view and complete a workout
 - View an exercise
 - Create, view and like posts
 - View personal profile and statistics
### Guest
- View exercise
- View posts
### SuperUser
 - Can view and complete a workout
 - Can view and create exercise
 - Can create tags
 - Can view all users, all user pages and all user statistics
 - View all posts, browse by user, create post and like

# Django Project Starter
## Prerequisites

- Python (3.6 or later)
- Django

## Commands
 - python -m venv venv
 - venv\Scripts\activate
 - pip install -r requirements.txt
 - cd fitnessApp

## Start the project
python manage.py runserver
