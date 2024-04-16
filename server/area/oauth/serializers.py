from rest_framework import serializers
from .models import OAuthToken

class OAuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = OAuthToken
        fields = '__all__'