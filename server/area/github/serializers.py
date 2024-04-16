from rest_framework import serializers

from oauth.models import OAuthToken

import requests

class GithubOAuthTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        user = validated_data.pop('user')
        access_token = validated_data.pop('access_token')
        if not user.is_authenticated:
            raise serializers.ValidationError("User not authenticated")
        if OAuthToken.objects.filter(owner=user, token_type="GH").exists():
            oauthToken = OAuthToken.objects.get(owner=user, token_type="GH")
            oauthToken.token = access_token
            oauthToken.save()
        else:
            oauthToken = OAuthToken.objects.create(owner=user, token_type="GH", token=access_token)
        return oauthToken

class GithubCodeSerializer(serializers.Serializer):
    code = serializers.CharField()

    def create(self, validated_data):
        code = validated_data.pop('code')
        client_id = '03a14c1310f3ffe9654f'
        client_secret = '24bdd6b35d5081d85dd6a4eaaff1f8f39666eaf9'
        url = "https://github.com/login/oauth/access_token"
        headers = {
            "Accept": "application/json"
        }
        data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code
        }
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            if 'access_token' not in response.json():
                raise serializers.ValidationError("Github returned no access_token")
            OAuthToken.objects.create(owner=self.context['request'].user, token_type="GH", token=response.json()['access_token'])
            return response.json()['access_token']
        else:
            raise serializers.ValidationError("Github returned code: " + str(response.status_code))