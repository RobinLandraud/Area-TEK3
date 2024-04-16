from rest_framework import serializers

from oauth.models import OAuthToken

class SpotifyOAuthTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        user = validated_data.pop('user')
        access_token = validated_data.pop('access_token')
        if not user.is_authenticated:
            raise serializers.ValidationError("User not authenticated")
        if OAuthToken.objects.filter(owner=user, token_type="SP").exists():
            oauthToken = OAuthToken.objects.get(owner=user, token_type="SP")
            oauthToken.token = access_token
            oauthToken.save()
        else:
            oauthToken = OAuthToken.objects.create(owner=user, token_type="SP", token=access_token)
        return oauthToken