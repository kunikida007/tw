from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    content = models.TextField(max_length=140)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
   
    def __str__(self):
        return self.content
         