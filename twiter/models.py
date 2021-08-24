from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    content = models.TextField(max_length=140)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

# ユーザーにツイート権限を付与
    def perms_user(self, user):
        return self.author == user

    def __str__(self):
        return self.content


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Post, related_name='favorites', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)
