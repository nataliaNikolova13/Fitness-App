from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s Post at {self.created_at}"
    

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    post = models.ForeignKey(Post,  on_delete=models.CASCADE)
    numLikes = models.PositiveIntegerField(default=0)

    def increment_count(self):
        self.count += 1
        self.save() 