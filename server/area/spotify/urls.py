from django.urls import path
from .views import RegisterSpotifyToken, getSpotifyToken, DeleteSpotifyToken

urlpatterns = [
    path('register-token/', RegisterSpotifyToken.as_view(), name="register-spotify-token"),
    path('get-token/', getSpotifyToken.as_view(), name="get-spotify-token"),
    path('delete-token/', DeleteSpotifyToken.as_view(), name="delete-spotify-token"),
]