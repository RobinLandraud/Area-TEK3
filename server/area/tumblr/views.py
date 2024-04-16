from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import TumblrOAuthTokenSerializer
from rest_framework.response import Response
from oauth.models import OAuthToken
import requests
from .reactions import create_tumblr_post
from django.contrib.auth.models import User

def response_code(code: int, data: dict = None):
    if not data:
        data = {}
    data['Access-Control-Allow-Origin'] = 'http://localhost:8081'
    data['Access-Control-Allow-Credentials'] = 'true'
    return Response(data, status=code)

class RegisterTumblrToken(generics.GenericAPIView):
    serializer_class = TumblrOAuthTokenSerializer
    def post(self, request):
        serializer = TumblrOAuthTokenSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        #token = OAuthToken.objects.filter(owner=request.user, token_type="TB").first()
        #print("WTF")
        #if token:
        #    print(token)
        #    #create_tumblr_post(token)
        #    post = create_blog_post(token.token, 'pyrroz.tumblr.com', 'text', '<p>This is the body of my first post.</p>', tags='firstpost, hello', state='published', title='My First Post')
        #    print(post)
        return response_code(200, {"msg": "Service added"})

class getTumblrToken(generics.GenericAPIView):
    serializer_class = TumblrOAuthTokenSerializer
    def get(self, request):
        if request.user.is_authenticated:
            token = OAuthToken.objects.filter(owner=request.user, token_type="TB").first()
            if token:
                return response_code(200, {"access_token": token.token})
            else:
                return response_code(404, {"error": "Token not found"})
        else:
            return response_code(401, {"error" :"Unauthorized"})
        
class DeleteTumblrToken(generics.GenericAPIView):
    serializer_class = TumblrOAuthTokenSerializer

    def delete(self, request):
        if request.user.is_authenticated:
            token = OAuthToken.objects.filter(owner=request.user, token_type="TB").first()
            if token:
                token.delete()
                return response_code(200, {"msg": "Token deleted"})
            else:
                return response_code(404, {"error": "Token not found"})
        else:
            return response_code(401, {"error" :"Unauthorized"})