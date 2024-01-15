from django.urls import path

from .views import list_all_posts, detail_post, post_of_user, create_post

urlpatterns = [
    path('', list_all_posts, name='list_all_posts'),
    path('create/', create_post, name='create_post'),
    path('<int:post_id>', detail_post, name='detail_post'),
    path('<str:username>/', post_of_user, name='user_posts'),
    
]