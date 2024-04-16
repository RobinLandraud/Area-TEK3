from django.urls import path
from .views import RegisterRedditToken, getRedditToken, DeleteRedditToken

urlpatterns = [
    path('register-token/', RegisterRedditToken.as_view(), name="register-reddit-token"),
    path('get-token/', getRedditToken.as_view(), name="get-reddit-token"),
    path('delete-token/', DeleteRedditToken.as_view(), name="delete-reddit-token"),
]