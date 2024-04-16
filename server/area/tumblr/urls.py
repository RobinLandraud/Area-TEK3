from django.urls import path
from .views import RegisterTumblrToken, getTumblrToken, DeleteTumblrToken

urlpatterns = [
    path('register-token/', RegisterTumblrToken.as_view(), name="register-tumblr-token"),
    path('get-token/', getTumblrToken.as_view(), name="get-tumblr-token"),
    path('delete-token/', DeleteTumblrToken.as_view(), name="delete-tumblr-token"),
]