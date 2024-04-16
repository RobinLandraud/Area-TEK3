from django.urls import path
from .views import AboutJson, RootRedirect

urlpatterns = [
    path('about.json', AboutJson.as_view(), name="about"),
    path('', RootRedirect.as_view(), name="root"),
]