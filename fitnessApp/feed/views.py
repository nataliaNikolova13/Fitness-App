from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post, Likes
from .forms import PostForm
from django.http import JsonResponse, HttpResponseForbidden

# Create your views here.
def list_all_posts(request):
    posts = Post.objects.all()
    return render(request, 'posts.html', {'posts': posts}) 

def detail_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'post_detail.html', {'post': post})

def post_of_user(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user)
    likes = Likes.objects.filter(user=user)
    return render(request, 'user_posts.html', {'posts': posts, 'likes': likes})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user 
            post.save()
            return redirect('/posts') 
    else:
        form = PostForm()

    return render(request, 'create_post.html', {'form': form})


def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if Likes.objects.filter(user=user, post=post).exists():
        return HttpResponseForbidden("You have already liked this post.")

    post.likes_set.create(user=user)

    return redirect(detail_post, post_id=post_id)