from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from functools import wraps
from .models import UserProfile
from django.core.exceptions import PermissionDenied



def guest_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view


def superuser_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "Permission Denied. You must be a superuser.")
            return redirect('/user/login')  

    return _wrapped_view


def user_owner_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        profile = get_object_or_404(UserProfile, id=kwargs['profile_id'])
        
        if request.user == profile.user:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "Permission Denied. You can only view your own profile.")
            return redirect('/')  

    return _wrapped_view


def user_owner_or_superuser_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except PermissionDenied:
            messages.error(request, "Permission Denied. You can only view your own profile or be a superuser.")
            return redirect('/')

    return _wrapped_view