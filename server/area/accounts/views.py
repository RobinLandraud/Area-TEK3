from django.http import JsonResponse
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, OAuthLoginSerializer, MailSerializer, ResponseUserLoggedSerializer, LoginUserSerializer
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes

from django.contrib.auth.models import User

from django.middleware.csrf import get_token
import requests

from drf_yasg.utils import swagger_auto_schema


def response_code(code: int, data: dict = None):
    if not data:
        data = {}
    data['Access-Control-Allow-Origin'] = 'http://localhost:8081'
    data['Access-Control-Allow-Credentials'] = 'true'
    return Response(data, status=code)


class UserAPI(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_id="user",
        operation_description="Get user",
        responses={200: UserSerializer},
    )
    def get(self, request, format=None):
        return Response({
            "user": UserSerializer(request.user, context=self.get_serializer_context()).data,
        })

# Register API


class RegisterAPI(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    @swagger_auto_schema(
        operation_id="register",
        operation_description="Register a new user",
        request_body=RegisterSerializer,
        responses={200: ResponseUserLoggedSerializer},
    )
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = []
    serializer_class = AuthTokenSerializer

    @swagger_auto_schema(
        operation_id="login",
        operation_description="Login a user",
        request_body=LoginUserSerializer,
        responses={200: ResponseUserLoggedSerializer},
    )
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class OAuthGoogle(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = []
    serializer_class = OAuthLoginSerializer

    @swagger_auto_schema(
        operation_id="oauth_google",
        operation_description="Login a user with Google",
        request_body=OAuthLoginSerializer,
        responses={200: ResponseUserLoggedSerializer},
    )
    def post(self, request, format=None):
        serializer = OAuthLoginSerializer(
            data=request.data, context={'token_type': "GL"})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(OAuthGoogle, self).post(request, format=None)


class OAuthReddit(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = OAuthLoginSerializer

    @swagger_auto_schema(
        operation_id="oauth_reddit",
        operation_description="Login a user with Reddit",
        request_body=OAuthLoginSerializer,
        responses={200: ResponseUserLoggedSerializer},
    )
    def post(self, request, format=None):
        print("OAuthReddit")
        serializer = OAuthLoginSerializer(
            data=request.data, context={'token_type': "RD"})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return response_code(200, {
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

class OAuthSpotify(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = OAuthLoginSerializer

    @swagger_auto_schema(
        operation_id="oauth_spotify",
        operation_description="Login a user with Spotify",
        request_body=OAuthLoginSerializer,
        responses={200: ResponseUserLoggedSerializer},
    )
    def post(self, request, format=None):
        print("OAuthSpotify")
        serializer = OAuthLoginSerializer(
            data=request.data, context={'token_type': "SP"})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return response_code(200, {
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class OAuthGithub(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = OAuthLoginSerializer

    @swagger_auto_schema(
        operation_id="oauth_github",
        operation_description="Login a user with Github",
        request_body=OAuthLoginSerializer,
        responses={200: ResponseUserLoggedSerializer},
    )
    def post(self, request, format=None):
        print("OAuthGithub")
        serializer = OAuthLoginSerializer(
            data=request.data, context={'token_type': "GH"})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return response_code(200, {
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

class OAuthTumblr(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = OAuthLoginSerializer

    @swagger_auto_schema(
        operation_id="oauth_tumblr",
        operation_description="Login a user with Tumblr",
        request_body=OAuthLoginSerializer,
        responses={200: ResponseUserLoggedSerializer},
    )
    def post(self, request, format=None):
        print("OAuthTumblr")
        serializer = OAuthLoginSerializer(
            data=request.data, context={'token_type': "TB"})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return response_code(200, {
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })