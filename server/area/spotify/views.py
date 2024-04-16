from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import SpotifyOAuthTokenSerializer
from rest_framework.response import Response
from oauth.models import OAuthToken
import requests
from .reactions import spotifyFirstReaction, spotifySecondReaction, spotifyThirdReaction, spotifyFourthReaction, execSpotifyReaction, save_show, add_track_to_queue
from drf_yasg.utils import swagger_auto_schema


def response_code(code: int, data: dict = None):
    if not data:
        data = {}
    data['Access-Control-Allow-Origin'] = 'http://localhost:8081'
    data['Access-Control-Allow-Credentials'] = 'true'
    return Response(data, status=code)

class RegisterSpotifyToken(generics.GenericAPIView):
    serializer_class = SpotifyOAuthTokenSerializer

    @swagger_auto_schema(
        operation_description="Register Spotify Token",
        request_body=SpotifyOAuthTokenSerializer,
        responses={
            200: "Service added",
            401: "Unauthorized",
            400: "Bad request",
        },
    )
    def post(self, request):
        serializer = SpotifyOAuthTokenSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response_code(200, {"msg": "Service added"})

class getSpotifyToken(generics.GenericAPIView):
    serializer_class = SpotifyOAuthTokenSerializer

    @swagger_auto_schema(
        operation_description="Get Spotify Token",
        responses={
            200: "access_token",
            401: "Unauthorized",
            404: "Token not found",
        },
    )
    def get(self, request):
        if request.user.is_authenticated:
            token = OAuthToken.objects.filter(owner=request.user, token_type="SP").first()
            if token:
                return response_code(200, {"access_token": token.token})
            else:
                return response_code(404, {"error": "Token not found"})
        else:
            return response_code(401, {"error" :"Unauthorized"})
        
class DeleteSpotifyToken(generics.GenericAPIView):
    serializer_class = SpotifyOAuthTokenSerializer

    def delete(self, request):
        if request.user.is_authenticated:
            token = OAuthToken.objects.filter(owner=request.user, token_type="SP").first()
            if token:
                token.delete()
                return response_code(200, {"msg": "Token deleted"})
            else:
                return response_code(404, {"error": "Token not found"})
        else:
            return response_code(401, {"error" :"Unauthorized"})