from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import generics, permissions
from drf_yasg.utils import swagger_auto_schema
from .models import OAuthToken
from .serializers import OAuthTokenSerializer

def response_code(code: int, data: dict = None):
    if not data:
        data = {}
    data['Access-Control-Allow-Origin'] = 'http://localhost:8081'
    data['Access-Control-Allow-Credentials'] = 'true'
    return Response(data, status=code)

class getTokensList(generics.GenericAPIView):
    serializer_class = None

    @swagger_auto_schema(
        operation_id="get_tokens",
        operation_description="Get all tokens of a user",
        responses={200: OAuthTokenSerializer},
    )
    def get(self, request):
        user = request.user
        tokens = OAuthToken.objects.filter(owner=user)
        informations = []
        for token in tokens:
            informations.append({
                "type": token.token_type,
                "token": token.token
            })
        return response_code(200, {"tokens" : informations})