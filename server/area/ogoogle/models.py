from django.db import models
from django.contrib.auth.models import User

class GmailCredential(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    token = models.CharField(max_length=2048)
    refresh_token = models.CharField(max_length=2048)
    expiry =  models.CharField(max_length=2048)

class Mail(models.Model):
    mail_id = models.CharField(max_length=2048)
    thread_id = models.CharField(max_length=2048)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)