from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post
from .forms import PostForm

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
    return render(request, 'user_posts.html', {'posts': posts})

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
