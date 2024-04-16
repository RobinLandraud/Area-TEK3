from django.urls import path
from .views import RegisterAPI, LoginAPI, OAuthGoogle, UserAPI #, SendMailView
from knox import views as knox_views
from . import views

urlpatterns = [
    path('user/', views.UserAPI.as_view(), name="user"),
    path('register/', RegisterAPI.as_view(), name="register"),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('oauth-google/', OAuthGoogle.as_view(), name='oauth google'),
    path('oauth-reddit/', views.OAuthReddit.as_view(), name='oauth reddit'),
    path('oauth-spotify/', views.OAuthSpotify.as_view(), name='oauth spotify'),
    path('oauth-github/', views.OAuthGithub.as_view(), name='oauth github'),
    path('oauth-tumblr/', views.OAuthTumblr.as_view(), name='oauth tumblr'),
    #path('google-mail/', SendMailView.as_view(), name="mail google")
]