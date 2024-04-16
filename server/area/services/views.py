from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Service
from django.contrib.auth.models import User
from oauth.models import OAuthToken
from .serializers import AddServiceSerializer, ServiceIdSerializer, ResponseServiceSerializer
from drf_yasg.utils import swagger_auto_schema
import json


def response_code(code: int, data: dict = None):
    if not data:
        data = {}
    data['Access-Control-Allow-Origin'] = 'http://localhost:8081'
    data['Access-Control-Allow-Credentials'] = 'true'
    return Response(data, status=code)


def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None


class deleteService(generics.GenericAPIView):
    serializer_class = ServiceIdSerializer

    @swagger_auto_schema(
        operation_id="delete_service",
        operation_description="Delete a service",
        request_body=ServiceIdSerializer,
        responses={200: "service deleted"},
    )
    def delete(self, request):
        user = request.user
        serializer = ServiceIdSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        service_id = serializer.validated_data['id']
        service = get_or_none(Service, id=service_id)
        if not service:
            return response_code(404, {"error": "Service not found"})
        if service.owner == user:
            service.delete()
            return response_code(200, {"success": "Service deleted"})
        else:
            return response_code(403, {"error": "You are not the owner of this service"})


class addService(generics.GenericAPIView):
    serializer_class = AddServiceSerializer

    @swagger_auto_schema(
        operation_id="add_service",
        operation_description="Add a service",
        request_body=AddServiceSerializer,
        responses={200: "service added"},
    )
    def post(self, request):
        serializer = AddServiceSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return response_code(200, {"success": "Service added"})
        return response_code(400, {"error": "Bad request"})


class updateService(generics.GenericAPIView):
    serializer_class = ResponseServiceSerializer

    @swagger_auto_schema(
        operation_id="update_service",
        operation_description="Update a service",
        request_body=ResponseServiceSerializer,
        responses={200: "service updated"},
    )
    def put(self, request):
        user = request.user
        service_id = request.data.get("id")
        service = get_or_none(Service, id=service_id)
        if not service:
            return response_code(404, {"error": "Service not found"})
        if service.owner == user:
            serializer = AddServiceSerializer(
                service, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return response_code(200, {"success": "Service updated"})
            return response_code(400, {"error": "Bad request"})
        else:
            return response_code(403, {"error": "You are not the owner of this service"})


class getServicesList(generics.GenericAPIView):
    serializer_class = None

    @swagger_auto_schema(
        operation_id="get_services",
        operation_description="Get all services of a user",
        responses={200: ResponseServiceSerializer},
    )
    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return response_code(401, "Unauthorized")
        services = Service.objects.filter(owner=user)
        informations = []
        for service in services:
            informations.append({
                "id": service.id,
                "name": service.name,
                "action": service.action,
                "name_action": service.name_action,
                "reaction": service.reaction,
                "name_reaction": service.name_reaction,
                "action_data": service.action_data,
                "reaction_data": service.reaction_data,
            })
        return response_code(200, {'services': informations})
