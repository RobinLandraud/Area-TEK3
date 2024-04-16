from django.urls import path
from .views import RegisterGithubToken, getGithubToken, RegisterGithubTokenFromCode, DeleteGithubToken

urlpatterns = [
    path('register-token/', RegisterGithubToken.as_view(), name="register-github-token"),
    path('get-token/', getGithubToken.as_view(), name="get-github-token"),
    path('register-token-from-code/', RegisterGithubTokenFromCode.as_view(), name="get-github-token-from-code"),
    path('delete-token/', DeleteGithubToken.as_view(), name="delete-github-token"),
]