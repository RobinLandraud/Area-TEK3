from django.urls import path
from .views import OAuthGoogleCode, GetToken, DeleteCredentials

urlpatterns = [
    path('get-token/', GetToken.as_view(), name="get-google-token"),
    path('register-token-from-code/', OAuthGoogleCode.as_view(), name="get-google-token-from-code"),
    path('delete-credentials/', DeleteCredentials.as_view(), name="delete-google-credentials"),
]