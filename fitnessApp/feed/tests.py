from django.test import TestCase
from django.urls import reverse
from .models import Post
from django.contrib.auth.models import User
from .forms import PostForm

class PostsViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='testpassword')
        self.post = Post.objects.create(user=self.user, title='Post 1', text='Content 1')
        self.post2 = Post.objects.create(user=self.user, title='Post 2', text='Content 2')

    def test_list_all_posts_view(self):
        url = reverse('list_all_posts')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts.html')
        posts = response.context['posts']
        self.assertEqual(len(posts), 2) 
        self.assertContains(response, 'Post 1')
        self.assertContains(response, 'Post 2')

    def test_detail_post_view_with_existing_post(self):
        url = reverse('detail_post', args=[self.post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post_detail.html')
        post = response.context['post']
        self.assertEqual(post, self.post)
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.text) 

    def test_detail_post_view_with_non_existing_post(self):
        url = reverse('detail_post', args=[9999])  
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_post_of_user_view(self):
        url = reverse('user_posts', args=[self.user.username])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_posts.html')
        posts = response.context['posts']
        self.assertEqual(len(posts), 2)
        self.assertContains(response, self.post.title)
