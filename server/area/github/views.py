from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import GithubOAuthTokenSerializer, GithubCodeSerializer
from rest_framework.response import Response
from oauth.models import OAuthToken
import requests
from .reactions import create_issue, create_pull_request
from drf_yasg.utils import swagger_auto_schema

def response_code(code: int, data: dict = None):
    if not data:
        data = {}
    data['Access-Control-Allow-Origin'] = 'http://localhost:8081'
    data['Access-Control-Allow-Credentials'] = 'true'
    return Response(data, status=code)

class RegisterGithubToken(generics.GenericAPIView):
    serializer_class = GithubOAuthTokenSerializer

    @swagger_auto_schema(
        operation_description="Register Github Token",
        request_body=GithubOAuthTokenSerializer,
        responses={
            200: "Service added",
            401: "Unauthorized",
            400: "Bad request",
        },
    )
    def post(self, request):
        serializer = GithubOAuthTokenSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response_code(200, {"msg": "Service added"})

class getGithubToken(generics.GenericAPIView):
    serializer_class = None

    @swagger_auto_schema(
        operation_description="Get Github Token",
        responses={
            200: "access_token",
            401: "Unauthorized",
            404: "Token not found",
        },
    )
    def get(self, request):
        if request.user.is_authenticated:
            token = OAuthToken.objects.filter(owner=request.user, token_type="GH").first()
            if token:
                return response_code(200, {"access_token": token.token})
            else:
                return response_code(404, {"error": "Token not found"})
        else:
            return response_code(401, {"error" :"Unauthorized"})
        
class RegisterGithubTokenFromCode(generics.GenericAPIView):
    serializer_class = GithubCodeSerializer

    @swagger_auto_schema(
        operation_description="Register Github Token from code",
        request_body=GithubCodeSerializer,
        responses={
            200: "access_token",
            401: "Unauthorized",
            400: "Bad request",
        },
    )
    def post(self, request):
        serializer = GithubCodeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        access_token = serializer.save()
        print("access_token : ", access_token)
        return response_code(200, {"access_token": access_token})
    
class DeleteGithubToken(generics.GenericAPIView):
    serializer_class = None

    @swagger_auto_schema(
        operation_description="Delete Github Token",
        responses={
            200: "Token deleted",
            401: "Unauthorized",
            404: "Token not found",
        },
    )
    def delete(self, request):
        if request.user.is_authenticated:
            token = OAuthToken.objects.filter(owner=request.user, token_type="GH").first()
            if token:
                token.delete()
                return response_code(200, {"msg": "Token deleted"})
            else:
                return response_code(404, {"error": "Token not found"})
        else:
            return response_code(401, {"error" :"Unauthorized"})