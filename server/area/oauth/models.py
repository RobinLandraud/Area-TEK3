from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class OAuthToken(models.Model):
    GOOGLE = 'GL'
    OTHER = 'OT'
    REDDIT = 'RD'
    SPOTIFY = 'SP'
    GITHUB = 'GH'
    TUMBLR = 'TB'
    TYPES = [
        (GOOGLE, 'Google OAuth2 token'),
        (REDDIT, 'Reddit OAuth2 token'),
        (SPOTIFY, 'Spotify OAuth2 token'),
        (GITHUB, 'Github OAuth2 token'),
        (TUMBLR, 'Tumblr OAuth2 token'),
        (OTHER, 'Other'),
    ]

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    token_type = models.CharField(
        max_length=2,
        choices=TYPES,
        default=OTHER
    )
    token = models.CharField(max_length=2048)