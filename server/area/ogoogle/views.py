from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import CodeSerializer, GmailCredentialSerializer
from .models import GmailCredential

from drf_yasg.utils import swagger_auto_schema

def response_code(code: int, data: dict = None):
    if not data:
        data = {}
    data['Access-Control-Allow-Origin'] = 'http://localhost:8081'
    data['Access-Control-Allow-Credentials'] = 'true'
    return Response(data, status=code)


class OAuthGoogleCode(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CodeSerializer

    @swagger_auto_schema(
        operation_id="oauth_google",
        operation_description="Register gmail auth",
        request_body=CodeSerializer,
        responses={
            200: "access_token"
        },       
    )
    def post(self, request, format=None):
        print("OAuthGoogle")
        serializer = CodeSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        access_token = serializer.validated_data['access_token']
        return response_code(200, {
            "access_token": access_token
        })
    
class GetToken(generics.GenericAPIView):
    serializer_class = None

    @swagger_auto_schema(
        operation_id="get_token",
        operation_description="Get gmail token",
        responses={
             200: "access_token",
             404: "Token not found"
        }
    )
    def get(self, request):
        if request.user.is_authenticated:
            credentials = GmailCredential.objects.filter(owner=request.user).first()
            if credentials:
                return response_code(200, {"access_token": credentials.token})
            else:
                return response_code(404, {"error": "Token not found"})
            
class DeleteCredentials(generics.GenericAPIView):
    serializer_class = None

    @swagger_auto_schema(
        operation_id="delete_credentials",
        operation_description="Delete gmail credentials",
        responses={
             200: "Credentials deleted",
             404: "Credentials not found"
        }
    )
    def delete(self, request):
        if request.user.is_authenticated:
            credentials = GmailCredential.objects.filter(owner=request.user).first()
            if credentials:
                credentials.delete()
                return response_code(200, {"message": "Credentials deleted"})
            else:
                return response_code(404, {"error": "Credentials not found"})
