from django.urls import path
from .views import user_login, user_logout, registration_view, user_list, user_detail, profile_edit

urlpatterns = [
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('register/', registration_view, name='registration_view'),
    path('<int:profile_id>', user_detail, name="user_detail"),
    path('edit/<int:profile_id>/', profile_edit, name='profile_edit'),
    path('', user_list, name="user_list")
   ]