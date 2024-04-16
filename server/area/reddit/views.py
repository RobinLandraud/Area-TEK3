from rest_framework import generics, permissions
from .serializers import RedditOAuthTokenSerializer
from rest_framework.response import Response
from oauth.models import OAuthToken

from .api import get_subscribed_subreddits
from drf_yasg.utils import swagger_auto_schema
#from .reactions import  submit_post, compose_message, follow_post, hide_link

def response_code(code: int, data: dict = None):
    if not data:
        data = {}
    data['Access-Control-Allow-Origin'] = 'http://localhost:8081'
    data['Access-Control-Allow-Credentials'] = 'true'
    return Response(data, status=code)

class RegisterRedditToken(generics.GenericAPIView):
    serializer_class = RedditOAuthTokenSerializer

    @swagger_auto_schema(
        operation_description="Register Reddit Token",
        request_body=RedditOAuthTokenSerializer,
        responses={
            200: "Service added",
            401: "Unauthorized",
            400: "Bad request",
        },
    )
    def post(self, request):
        serializer = RedditOAuthTokenSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        #token = OAuthToken.objects.filter(owner=request.user, token_type="RD").first()
        return response_code(200, {"msg": "Service added"})

class getRedditToken(generics.GenericAPIView):
    serializer_class = None

    @swagger_auto_schema(
        operation_description="Get Reddit Token",
        responses={
            200: "access_token",
            401: "Unauthorized",
            404: "Token not found",
        },
    )
    def get(self, request):
        if request.user.is_authenticated:
            token = OAuthToken.objects.filter(owner=request.user, token_type="RD").first()
            if token:
                return response_code(200, {"access_token": token.token})
            else:
                return response_code(404, {"error": "Token not found"})
        else:
            return response_code(401, {"error" :"Unauthorized"})
        
class DeleteRedditToken(generics.GenericAPIView):
    serializer_class = None

    @swagger_auto_schema(
        operation_description="Delete Reddit Token",
        responses={
            200: "Token deleted",
            401: "Unauthorized",
            404: "Token not found",
        },
    )
    def delete(self, request):
        if request.user.is_authenticated:
            token = OAuthToken.objects.filter(owner=request.user, token_type="RD").first()
            if token:
                token.delete()
                return response_code(200, {"msg": "Token deleted"})
            else:
                return response_code(404, {"error": "Token not found"})
        else:
            return response_code(401, {"error" :"Unauthorized"})