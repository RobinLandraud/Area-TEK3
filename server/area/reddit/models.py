from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Subreddit(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    subscribers = models.IntegerField(blank=True, null=True)
    created = models.CharField(max_length=120, blank=True, null=True)
    url = models.CharField(max_length=300, blank=True, null=True)
    img_src = models.CharField(max_length=300, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name