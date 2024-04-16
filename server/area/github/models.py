from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Repository(models.Model):
    repo_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    repo_owner = models.CharField(max_length=100)
    repo_id = models.CharField(max_length=100)
    private = models.BooleanField()
    url = models.CharField(max_length=1000)
    commits_url = models.CharField(max_length=1000)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='github_repos')

    def __str__(self):
        return self.name

class Commit(models.Model):
    sha = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    url = models.CharField(max_length=1000)
    message = models.CharField(max_length=1000)
    date = models.CharField(max_length=1000)
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE, related_name='commits')

    def __str__(self):
        return self.sha