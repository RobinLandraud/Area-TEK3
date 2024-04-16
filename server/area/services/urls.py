from django.urls import path
from .views import getServicesList, addService, deleteService, updateService

urlpatterns = [
    path('get/', getServicesList.as_view(), name="get-services"),
    path('add/', addService.as_view(), name="add-service"),
    path('delete/', deleteService.as_view(), name="delete-service"),
    path('update/', updateService.as_view(), name="update-service"),
]