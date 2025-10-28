from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    text = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    liked_by = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    favorited_by = models.ManyToManyField(User, related_name='favorite_posts', blank=True)

    def __str__(self):
        return self.title
