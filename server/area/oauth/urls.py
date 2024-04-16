from django.urls import path
from .views import getTokensList

urlpatterns = [
    path('get-tokens/', getTokensList.as_view(), name="get-tokens"),
]